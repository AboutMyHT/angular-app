"""All tests in this file are for the session lambda function.

Related requirements:
    - 3.3.x
    - 5.0.0
    - 5.5.0
"""

import json

from session import app

from amht_custom.sqla.models.tables import User, UserSession


def test_session_missing_token(mocker):
    """Test 1 | Test that the session_token is required"""
    mocker.patch("session.app.get_rds_session")
    body = json.dumps({})  # No session token provided
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert response["body"] == '"session_token is required!"'


def test_session_token_invalid(mocker):
    """Test 2 | Test that an invalid session token returns a 401 status code"""
    mocker.patch("session.app.get_rds_session")
    mocker.patch("session.app.validate_token", return_value=False)
    body = json.dumps({"session_token": "invalidtoken"})
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 401
    assert response["body"] == '"Invalid session token"'


def test_successful_session_token_validation(mocker):
    """Test 3 | Test that a valid session token returns a 200 status code"""
    mocker.patch("session.app.get_rds_session")
    mocker.patch("session.app.validate_token", return_value=True)
    mocker.patch(
        "session.app.get_user_session",
        return_value=UserSession(
            user=User(
                email="test@test.com",
                first_name="Test",
                last_name="User",
                zip_code="12345",
            )
        ),
    )
    body = json.dumps({"session_token": "validtoken"})
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    expected_user_info = {
        "email": "test@test.com",
        "first_name": "Test",
        "last_name": "User",
        "zip_code": "12345",
        "bio_info": None,
        "email_verified": None,
        "needs_password_reset": None,
    }

    assert json.loads(response["body"])["user"] == expected_user_info


def test_session_token_validation_raises_value_error(mocker):
    """Test 4 | Test that a ValueError is raised when the session token is invalid"""
    mocker.patch("session.app.get_rds_session")
    mocker.patch(
        "session.app.validate_token", side_effect=ValueError("Invalid session token")
    )
    body = json.dumps({"session_token": "validtoken"})
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 401
    assert response["body"] == '"Invalid session token"'


def test_lambda_handler_invalid_json(mocker):
    """Test 5 | Test that the lambda handler returns a 400 status code when the JSON body is invalid."""
    mocker.patch("session.app.get_rds_session")

    apigw_event = {"body": "invalid json"}

    ret = app.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 400
    assert ret["body"] == '"Invalid JSON body."'
