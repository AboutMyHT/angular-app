import json
import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import api_response
from amht_custom.db_utils.users import (
    get_user,
    check_password,
)


logger = logging.getLogger()


def lambda_handler(event, context):
    """
    If running API locally, use http://localhost:4201/signin
    Otherwise, https://api.aboutmyhometown.com/signin

    Examples
    --------
        requests.post("http://localhost:4201/signin", json={"email":"tester@test.com", "password":"passwd"}).content
            > b'"Invalid email or password!"
            > b'{"user": {"email": "tester@test.com", "first_name": "Bob", "last_name": "the Builder", "zip_code": "61554"}}'

        requests.post("https://api.aboutmyhometown.com/signin", json={"email":"tester@test.com", "password":"passwd"}).content
            > b'"Invalid email or password!"
            > b'{"user": {"email": "tester@test.com", "first_name": "Bob", "last_name": "the Builder", "zip_code": "61554"}}'

    Return
    -------
        "Invalid email or password!" if the email and password do not match OR if the user does not exist.
        User information if the email and password match.
    """

    # Check if the request body is a valid JSON
    try:
        post_body = json.loads(event.get("body"))
    except json.JSONDecodeError:
        return api_response("Invalid JSON body.", 400)

    # Check if the required parameters are present
    if post_body.get("email") is None or post_body.get("password") is None:
        return api_response(
            "The email and password parameters are required to log in!",
            400,
        )

    try:
        with get_rds_session()() as session:
            is_valid_password = check_password(
                session, post_body["email"], post_body["password"]
            )

            if is_valid_password:
                user_in_db = get_user(session, post_body["email"])

                return api_response(
                    {
                        "user": {
                            "email": user_in_db.email,
                            "first_name": user_in_db.first_name,
                            "last_name": user_in_db.last_name,
                            "zip_code": user_in_db.zip_code,
                        },
                    },
                    200,
                )
            else:
                return api_response(
                    "Invalid email or password!",
                    401,
                )

    except ValueError as error:
        return api_response(
            str(error),
            400,
        )

    return api_response("An unexpected error occured!", 500)
