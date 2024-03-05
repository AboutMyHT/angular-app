import os

import boto3
from amht_custom.mysql import get_mysql_db

from mysql.connector.connection import MySQLConnection
from mysql.connector.pooling import PooledMySQLConnection, CMySQLConnection

def get_rds_connection(use_ssl: bool = True) -> PooledMySQLConnection | MySQLConnection | CMySQLConnection:
    """
    Get a connection to the RDS database
    """
    # Get authentication token from RDS
    rds_client = boto3.client("rds")
    auth_token = rds_client.generate_db_auth_token(
        os.environ["DB_HOST"], 3306, os.environ["DB_USER"]
    )

    print("response from generate_db_auth_token")
    print(auth_token)

    # Construct SSL
    ssl = {"ca": "/opt/python/us-east-2-bundle.pem"}
    with open(ssl["ca"], 'r') as f:
        print(f.read())

    # Create connection
    return get_mysql_db(
        username=os.environ["DB_USER"],
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        password=auth_token,
        port=3306,
        ssl=ssl if use_ssl else {},
    )