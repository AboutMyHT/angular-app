"""
    Purpose: This is the core module for the AboutMyHometown custom Python library.
        This module contains methods for interacting with the RDS database through
            ORM using SQLAlchemy.
        This module also contains the code for session management, such as token
            generation, user authentication, and session creation.
    
    Requirements: 3.x; 5.x
"""
import os
import logging

import boto3
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
        ENGINE = _get_create_engine(
            username="root",
            host="172.17.0.2",
            database="mydb",
            password="localpass",
            port=3306,
        )
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
