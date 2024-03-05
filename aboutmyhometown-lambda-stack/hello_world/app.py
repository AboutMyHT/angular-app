import logging
import json

from amht_custom import get_rds_connection

from mysql.connector.connection import MySQLConnection

logger = logging.getLogger()


def lambda_handler(event, context):
    """
    Main entry of the AWS Lambda function.
    """
    with get_rds_connection() as db_connection:
        logger.info("Hello world!")
        return {
            "statusCode": 200,
            "body": json.dumps({"num": prepare_and_execute_query(db_connection)}),
        }


def prepare_and_execute_query(
    db_connection: MySQLConnection,
):
    """
    Execute the query on the MySQL database
    """

    with db_connection.cursor() as cur:
        try:
            sql_query = "select * from information_schema.tables;"

            items = cur.execute(sql_query)
            db_connection.commit()

            return items

        except Exception as e:
            db_connection.rollback()
            raise e
