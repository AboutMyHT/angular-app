import json
import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import api_response
from amht_custom.db_utils.users import (
    create_user,
    get_user,
)


logger = logging.getLogger()


def lambda_handler(event, context):
    """
    If running API locally, use http://localhost:4201/signup
    Otherwise, https://api.aboutmyhometown.com/signup

    Examples
    --------
        requests.post("http://localhost:4201/signup", json={"email":"test@test.com", "password":"pass"}).content
            > b'"The email, password, and zip code parameters are required."'

        requests.post("https://api.aboutmyhometown.com/signup", json={"email":"test@test.com", "password":"pass", "zip_code":"61554"}).content
            > b'"User already exists. Please use a different email."'

        requests.post("https://api.aboutmyhometown.com/signup", json={"email":"test123@test.com", "password":"passwd", "zip_code":"61554"}).content
            > b'{"user": {"email": "test@test.com", "first_name": null, "last_name": null, "zip_code": "61554"}}'

        requests.post("https://api.aboutmyhometown.com/signup", json={"email":"test123@test.com", "first_name": "bob", "password":"passwd", "zip_code":"61554"}).content
            > b'{"user": {"email": "test@test.com", "first_name": "bob", "last_name": null, "zip_code": "61554"}}'

    Return
    -------
        "The email, password, and zip code parameters are required." if the email, password, or zip code are missing.
        "User already exists. Please use a different email." if the user already exists.
        User information if the user is created successfully.
    """

    # Check if the request body is a valid JSON
    try:
        post_body = json.loads(event.get("body"))
    except json.JSONDecodeError:
        return api_response("Invalid JSON body.", 400)

    # Check if the required parameters are present
    if (
        post_body.get("email") is None
        or post_body.get("password") is None
        or post_body.get("zip_code") is None
    ):
        return api_response(
            "The email, password, and zip code parameters are required.",
            400,
        )

    # Create a new user
    try:
        with get_rds_session()() as session:
            create_user(
                session=session,
                email=post_body["email"],
                zip_code=post_body["zip_code"],
                password_rawstring=post_body["password"],
                first_name=post_body.get("first_name"),
                last_name=post_body.get("last_name"),
            )

            # Get the user from the database to confirm the creation
            user_in_db = get_user(session, post_body["email"])

            if user_in_db:
                # Return the user information
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
    except ValueError as error:
        return api_response(
            str(error),
            400,
        )

    return api_response("An unexpected error occured!", 500)
