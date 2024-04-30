"""All tests in this file are for the updateuser lambda function.

Related requirements:
    - 3.3.6
    - 4.6.0
    - 5.6.0
"""

import json

from updateuser import app

from amht_custom.sqla.models.tables import User, UserSession


def test_update_user_missing_parameters(mocker):
    """Test 15 | Test that missing session token or zip code parameters returns a 400 status code."""
    mocker.patch("updateuser.app.get_rds_session")
    body = json.dumps(
        {"session_token": "1231213-1231213-1231232-3122323"}
    )  # Missing zip code
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert (
        response["body"] == '"The session token and zip code parameters are required."'
    )


def test_update_user_invalid_session_token(mocker):
    """Test 16 | Test that an invalid session token returns a 400 status code."""
    mocker.patch("updateuser.app.get_rds_session")
    mocker.patch(
        "updateuser.app.get_user_session", return_value=UserSession(email=None)
    )  # Invalid session token
    body = json.dumps({"session_token": "invalidtoken", "zip_code": "61554-4220"})
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert response["body"] == '"Session token is invalid!"'


def test_update_user_successful(mocker):
    """Test 17 | Test that a successful update returns a 200 status code."""
    mocker.patch("updateuser.app.get_rds_session")
    mocker.patch(
        "updateuser.app.get_user_session",
        return_value=UserSession(email="test@test.com"),
    )
    mocker.patch("updateuser.app.modify_user")
    mocker.patch(
        "updateuser.app.get_user",
        return_value=User(
            email="test@test.com",
            zip_code="61554-4220",
            first_name="Bob",
            last_name="Builder",
        ),
    )
    body = json.dumps(
        {
            "session_token": "1231213-1231213-1231232-3122323",
            "zip_code": "61554-4220",
            "first_name": "Bob",
            "last_name": "Builder",
        }
    )
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    expected_user_info = {
        "email": "test@test.com",
        "first_name": "Bob",
        "last_name": "Builder",
        "zip_code": "61554-4220",
        "bio_info": None,
        "email_verified": None,
        "needs_password_reset": None,
    }

    assert json.loads(response["body"])["user"] == expected_user_info


def test_update_user_does_not_exist(mocker):
    """Test 18 | Test that a user that does not exist returns a 400 status code."""
    mocker.patch("updateuser.app.get_rds_session")
    mocker.patch(
        "updateuser.app.get_user_session",
        return_value=UserSession(email="nonexistent@test.com"),
    )
    mocker.patch(
        "updateuser.app.modify_user", side_effect=ValueError("User does not exist!")
    )
    body = json.dumps({"session_token": "validtoken", "zip_code": "61554-4220"})
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert response["body"] == '"User does not exist!"'


def test_update_user_invalid_json(mocker):
    """Test 19 | Test that invalid JSON returns a 400 status code."""
    mocker.patch("updateuser.app.get_rds_session")
    event = {"body": "invalid json"}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert response["body"] == '"Invalid JSON body."'
