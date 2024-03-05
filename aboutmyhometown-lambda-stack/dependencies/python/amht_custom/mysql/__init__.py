"""mysql - This module contains all of the mysql connector logic

Examples
----------
>>> from csa_python.config import settings
>>> from csa_python.mysql import get_mysql_db
>>> settings.configure(FORCE_ENV_FOR_DYNACONF="testing")

>>> try:
...     connection = get_mysql_db(
...         username=settings["DATABASE.username"],
...         password=str(settings["DATABASE.password"]),
...         host=settings["DATABASE.host"],
...         port=settings["DATABASE.port"],
...         database=settings["DATABASE.database"],
...     )
...     with connection.cursor() as cursor:
...         cursor.execute("select * from null")
... except:
...     print("Failed because testing")
Failed because testing
"""

# pylint: disable=import-error
import logging
from typing import Dict

import mysql.connector

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection, CMySQLConnection

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_connections: Dict[str, PooledMySQLConnection | MySQLConnection | CMySQLConnection] = {}


def _get_create_connection(
    username: str,
    host: str,
    database: str,
    password: str,
    port: int = 3306,
    conn_uid: int = 0,
    ssl: Dict[str, str] = {},
) -> PooledMySQLConnection | MySQLConnection | CMySQLConnection:
    """This method creates the connection object and adds it to the _connections variable
        for access.
    It will create a connection if one does not exist and retrieve it if it
        does.
    """
    connection_locator = f"{username}_{host}_{database}_{conn_uid}"

    exists = _connections.get(connection_locator, None)
    if exists:
        if exists.is_connected():
            logger.debug("MySQL Connection %s is open, grabbing...", connection_locator)
            return exists

    logger.debug(
        "MySQL Connection %s was not open, creating new...", connection_locator
    )

    _connections[connection_locator] = mysql.connector.connect(
        user=username,
        passwd=str(password),
        host=host,
        port=port,
        database=database,
        ssl_ca=ssl.get("ca")
        
    )
    return _connections[connection_locator]


def get_mysql_db(
    username: str,
    host: str,
    database: str,
    password: str,
    port: int = 3306,
    conn_uid: int = 0,
    ssl: Dict[str, str] = {},
) -> PooledMySQLConnection | MySQLConnection | CMySQLConnection:
    """Takes connection information and returns a MySQL connector

    Parameters
    ----------
        username: str
            The user to create a database connection with
        host: str
            The host to connect to
        datbase: str
            The name of the database schema
        password: str
            User's password (default None)
        port: int
            The port to conenct to (default 3306)
        conn_uid: int
            A unique identifier for grabbing specific connections (default 0)

    Returns
    ----------
        mysql.connector
    """
    connection_object = _get_create_connection(
        username=username,
        host=host,
        database=database,
        password=password,
        port=port,
        conn_uid=conn_uid,
        ssl=ssl,
    )

    return connection_object
