"""sqla - This module contains all of the SQL Alchemy logic

Examples
----------
>>> import sqlalchemy
>>> from csa_python.sqla.models import LogEntry
>>> from csa_python.config import settings
>>> settings.configure(FORCE_ENV_FOR_DYNACONF="testing")

>>> settings_connection = settings.mysql.get("conn")
>>> session_maker = get_sessionmaker(
...     username=settings_connection.username,
...     password=str(settings_connection.password),
...     host=settings_connection.testing_host,
...     database=settings_connection.database,
...     port=settings_connection.get("port", 3306),
...     echo=False,
... )

>>> with session_maker() as session:
...     try:
...         session.add(LogEntry())
...         session.commit()
...     except sqlalchemy.exc.OperationalError:
...         print("Failed because testing")
Failed because testing
"""

import logging
from typing import Dict

from sqlalchemy import create_engine, URL, Engine

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_engines: Dict[str, Engine] = {}


def _create_engine_url(
    username: str,
    host: str,
    database: str,
    password: str | None = None,
    port: int | None = None,
    dialect: str = "mysql",
    driver: str = "pymysql",
) -> URL:
    """This method generates the engine URL given parameters"""
    url_object = URL.create(
        f"{dialect}+{driver}",
        username=username,
        password=password,  # plain (unescaped) text
        host=host,
        database=database,
        port=port,
    )
    return url_object


def _get_create_engine(
    username: str,
    host: str,
    database: str,
    password: str | None = None,
    port: int | None = None,
    dialect: str = "mysql",
    driver: str = "pymysql",
    echo: bool = False,
    connect_args: Dict[str, str] | None = None,
) -> Engine:
    """This method creates the engine object and adds it to the _engines variable
        for access.
    It will create an engine if one does not exist and retrieve it if it
        does.
    """
    engine_locator = f"{username}_{host}_{database}"

    engine_url = _create_engine_url(
        username, host, database, password, port, dialect, driver
    )

    exists = _engines.get(engine_locator, None)
    if exists:
        logger.debug("SQLA Connection %s is open, grabbing...", engine_locator)
        return exists

    logger.debug("SQLA Connection %s was not open, creating new...", engine_locator)
    _engines[engine_locator] = create_engine(
        engine_url, echo=echo, connect_args=connect_args or {}
    )
    return _engines[engine_locator]
