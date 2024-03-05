import os
import logging

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from amht_custom.sqla.models.tables import Base
from amht_custom.sqla import _get_create_engine

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

NOT_PROD = os.getenv("ENVIRONMENT", None) != "production"


def get_rds_session() -> sessionmaker:
    """
    Get a connection to the RDS database
    """

    if NOT_PROD:
        ENGINE = create_engine("sqlite:////tmp/local_database.db")
    else:
        # Get authentication token from RDS
        rds_client = boto3.client("rds")
        auth_token = rds_client.generate_db_auth_token(
            os.environ["DB_HOST"], 3306, os.environ["DB_USER"]
        )

        # Construct SSL
        ssl = {"ssl_ca": "/opt/python/us-east-2-bundle.pem"}

        logger.info("Creating connection to RDS database...")

        # Create connection
        ENGINE = _get_create_engine(
            username=os.environ["DB_USER"],
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            password=auth_token,
            port=3306,
            connect_args=ssl,
        )

    Base.metadata.create_all(ENGINE)

    return sessionmaker(ENGINE)
