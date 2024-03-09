import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import api_response
from amht_custom.db_utils.users import list_users


logger = logging.getLogger()


def lambda_handler(event, context):
    """
    Main entry of the AWS Lambda function.
    """
    get_parameters = event.get("queryStringParameters") or {}

    if (
        get_parameters.get("temp_endpoint") is None
        or get_parameters.get("temp_endpoint") != "temp_endpoint"
    ):
        return api_response(
            "Not available",
            400,
        )

    try:
        with get_rds_session()() as session:
            users = [user.email for user in list_users(session)]
            return api_response(
                {
                    "users": users,
                },
                200,
            )
    except ValueError as error:
        return api_response(
            str(error),
            400,
        )
