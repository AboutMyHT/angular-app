import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import invalid_response, valid_response
from amht_custom.db_utils.users import (
    create_user,
    get_user,
    check_password,
    modify_user,
)


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
            new_user = create_user(
                session=session,
                email=get_parameters["email"],
                zip_code=get_parameters["zip_code"],
                password_rawstring=get_parameters["password"],
                first_name=get_parameters.get("first_name"),
                last_name=get_parameters.get("last_name"),
            )

            user_in_db = get_user(session, get_parameters["email"])

            modify_user(
                session=session,
                email=get_parameters["email"],
                zip_code="12394",
                first_name="John",
                last_name="Doe",
            )

            if new_user:
                return valid_response(
                    {
                        "message": "User created successfully",
                        "user": {
                            "email": user_in_db.email,
                            "first_name": user_in_db.first_name,
                            "last_name": user_in_db.last_name,
                            "zip_code": user_in_db.zip_code,
                        },
                        "password_correct": check_password(
                            session,
                            get_parameters["email"],
                            get_parameters["password"],
                        ),
                    },
                    200,
                )
    except ValueError as error:
        return invalid_response(
            str(error),
            400,
        )

    return invalid_response("An unexpected error occured!", 500)
