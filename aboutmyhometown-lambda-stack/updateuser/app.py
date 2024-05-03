"""
    Purpose: This is the Lambda function that handles the /updateuser API endpoint.
    Requirements: 5.6.0
"""
import json
import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import api_response
from amht_custom.db_utils.sessions import get_user_session
from amht_custom.db_utils.users import (
    modify_user,
    get_user,
)


logger = logging.getLogger()


def lambda_handler(event, context):
    """
    If running API locally, use http://localhost:4201/updateuser
    Otherwise, https://api.aboutmyhometown.com/updateuser

    Examples
    --------
        requests.post("http://localhost:4201/signup", json={"session_token":"1231213-1231213-1231232-3122323", "zip_code":"61554-4220"}).content
            > b'{"user": {"email": "test@test.com", "first_name": null, "last_name": null, "zip_code": "61554"}}'

        requests.post("https://api.aboutmyhometown.com/updateuser", json={"session_token":"1231213-1231213-1231232-3122323", "zip_code":"61554-4220"}).content
            > b'{"user": {"email": "test@test.com", "first_name": null, "last_name": null, "zip_code": "61554"}}'

    Return
    -------
        "The session token and zip code parameters are required." if the session token or zip code are missing.
        "Session token is invalid!" if the session token is invalid.
        "User does not exist!" if the user does not exist.
        User information if the user is updated successfully.
    """

    # Check if the request body is a valid JSON
    try:
        post_body = json.loads(event.get("body"))
    except json.JSONDecodeError:
        return api_response("Invalid JSON body.", 400)

    # Check if the required parameters are present
    if post_body.get("session_token") is None or post_body.get("zip_code") is None:
        return api_response(
            "The session token and zip code parameters are required.",
            400,
        )

    # Create a new user
    try:
        with get_rds_session()() as session:
            # Get the email address for the token
            user_session = get_user_session(
                session=session, session_token=post_body["session_token"]
            )

            # Check if the session token is valid
            if user_session.email is None:
                return api_response(
                    "Session token is invalid!",
                    400,
                )

            # Make the modifications to the user
            modify_user(
                session=session,
                email=user_session.email,
                zip_code=post_body["zip_code"],
                first_name=post_body.get("first_name"),
                last_name=post_body.get("last_name"),
                bio_info=post_body.get("bio_info"),
            )

            # Get the user from the database to confirm the modification
            user_in_db = get_user(session, user_session.email)

            if user_in_db:
                # Return the user information
                logger.info("User updated successfully.")
                return api_response(
                    {
                        "user": user_in_db.as_dict(),
                    },
                    200,
                )
    except ValueError as error:
        logger.info(f"Error: {error}")
        return api_response(
            "User does not exist!",
            400,
        )

    return api_response("An unexpected error occured!", 500)
