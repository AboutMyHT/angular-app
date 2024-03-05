import time
import json
import logging

from amht_custom import get_rds_session
from amht_custom.sqla.models.tables import User

from sqlalchemy.orm import Session

logger = logging.getLogger()


def lambda_handler(event, context):
    """
    Main entry of the AWS Lambda function.
    """
    with get_rds_session()() as session:
        return {
            "statusCode": 200,
            "body": json.dumps({"users": get_all_users(session)}),
        }


def get_all_users(
    session: Session,
):
    """
    Execute the query on the MySQL database
    """

    new_user = User(
        name="John Doe",
        email="test@test.com" + str(time.time())[-4:],
        password_hash="test",
    )
    session.add(new_user)
    session.commit()

    users = session.query(User).all()

    user_str = []
    for user in users:
        user_str.append(f"Name: {user.name}, Email: {user.email}")

    return user_str
