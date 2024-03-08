import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import invalid_response, valid_response
from amht_custom.db_utils.users import create_user


logger = logging.getLogger()


def lambda_handler(event, context):
    """
    Main entry of the AWS Lambda function.
    """
    get_parameters = event.get("queryStringParameters") or {}

    if (
        get_parameters.get("email") is None
        or get_parameters.get("password") is None
        or get_parameters.get("zip_code") is None
    ):
        return invalid_response(
            "The email, password, and zip code parameters are required.",
            400,
        )

    try:
        with get_rds_session()() as session:
            return valid_response(
                {
                    "new_user": create_user(
                        session=session,
                        email=get_parameters["email"],
                        zip_code=get_parameters["zip_code"],
                        password_rawstring=get_parameters["password"],
                        first_name=get_parameters.get("first_name"),
                        last_name=get_parameters.get("last_name"),
                    )
                },
                200,
            )
    except ValueError as error:
        return invalid_response(
            str(error),
            400,
        )
