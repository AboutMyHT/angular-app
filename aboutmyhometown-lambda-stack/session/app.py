import json
import logging

from amht_custom import get_rds_session
from amht_custom.http_utils import api_response

# from amht_custom.db_utils.users import (
#     get_user,
#     check_password,
# )
from amht_custom.db_utils.sessions import validate_token, get_user_session


logger = logging.getLogger()


def lambda_handler(event, context):
    """
    If running API locally, use http://localhost:4201/session
    Otherwise, https://api.aboutmyhometown.com/session

    Takes a session token and returns the associated user information.

    Return
    -------
        User information if the session token exists.
        "Invalid session token" if the session token does not exist.
    """

    # Check if the request body is a valid JSON
    try:
        post_body = json.loads(event.get("body"))
    except json.JSONDecodeError:
        return api_response("Invalid JSON body.", 400)

    # Check if the required parameters are present
    if post_body.get("session_token") is None:
        return api_response(
            "session_token is required!",
            400,
        )

    try:
        with get_rds_session()() as session:
            input_token = post_body.get("session_token")

            logger.debug("Validating session token.")
            is_valid_token = validate_token(session=session, session_token=input_token)

            if is_valid_token:
                user_session_in_db = get_user_session(session, input_token)
                user_from_session = user_session_in_db.user

                print(user_session_in_db)

                return api_response(
                    {
                        "user": user_from_session.as_dict(),
                    },
                    200,
                )
            else:
                logger.info("Session is invalid!")
                return api_response(
                    "Invalid session token",
                    401,
                )

    except ValueError as error:
        logger.info(f"Error: {error}")
        return api_response(
            "Invalid session token",
            401,
        )

    return api_response("An unexpected error occured!", 500)
