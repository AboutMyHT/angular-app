import boto3
import logging
import pymysql
import os
import json

logger = logging.getLogger()

print("starting")


# Get authentication token from RDS
rds_client = boto3.client("rds")
auth_token = rds_client.generate_db_auth_token(
    os.environ["DB_HOST"], 3306, os.environ["DB_USER"]
)

print("response from generate_db_auth_token")
print(auth_token)

# Construct SSL
ssl = {"ca": "/opt/python/us-east-2-bundle.pem"}

# Create connection
db_connection = pymysql.connect(
    host=os.environ["DB_HOST"],
    user=os.environ["DB_USER"],
    passwd=auth_token,
    port=3306,
    db=os.environ["DB_NAME"],
    charset="utf8",
    ssl=ssl,
    connect_timeout=5,
)

logger.debug("SUCCESS: Connection to MySQL database succeeded")


def lambda_handler(event, context):
    """
    Main entry of the AWS Lambda function.
    """
    logger.info("Hello world!")
    return prepare_and_execute_query()


def prepare_and_execute_query():
    """
    Execute the query on the MySQL database
    """

    with db_connection.cursor(pymysql.cursors.DictCursor) as cur:
        try:
            sql_query = "select * from information_schema.tables;"

            items = cur.execute(sql_query)
            db_connection.commit()

            return items

        except Exception as e:
            db_connection.rollback()
            raise e
