import json
import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import api_response
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

    try:
        post_body = json.loads(event.get("body"))
    except json.JSONDecodeError:
        return api_response("Invalid JSON body.", 400)

    if (
        post_body.get("email") is None
        or post_body.get("password") is None
        or post_body.get("zip_code") is None
    ):
        return api_response(
            "The email, password, and zip code parameters are required.",
            400,
        )

    try:
        with get_rds_session()() as session:
            new_user = create_user(
                session=session,
                email=post_body["email"],
                zip_code=post_body["zip_code"],
                password_rawstring=post_body["password"],
                first_name=post_body.get("first_name"),
                last_name=post_body.get("last_name"),
            )

            user_in_db = get_user(session, post_body["email"])

            modify_user(
                session=session,
                email=post_body["email"],
                zip_code="12394",
                first_name="John",
                last_name="Doe",
            )

            if new_user:
                return api_response(
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
                            post_body["email"],
                            post_body["password"],
                        ),
                    },
                    200,
                )
    except ValueError as error:
        return api_response(
            str(error),
            400,
        )

    return api_response("An unexpected error occured!", 500)
