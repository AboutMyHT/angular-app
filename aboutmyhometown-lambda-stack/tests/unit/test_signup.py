"""All tests in this file are for the signup lambda function.

Related requirements:
    - 2.0.x
    - 2.1.x
    - 3.0.0
    - 3.2.x
    - 5.3.0
"""

import json

from signup import app

from amht_custom.sqla.models.tables import User


def test_signup_missing_parameters(mocker):
    """Test 10 | Test that missing email, password, or zip code parameters returns a 400 status code."""
    mocker.patch("signup.app.get_rds_session")
    body = json.dumps(
        {"email": "test@test.com", "password": "pass"}
    )  # Missing zip code
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert (
        response["body"]
        == '"The email, password, and zip code parameters are required."'
    )

    body = json.dumps({"password": "pass"})  # Missing email
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert (
        response["body"]
        == '"The email, password, and zip code parameters are required."'
    )


def test_user_already_exists(mocker):
    """Test 11 | Test that a user already existing in the database returns a 400 status code."""
    mocker.patch("signup.app.get_rds_session")
    mocker.patch("signup.app.create_user", side_effect=ValueError("User exists"))
    body = json.dumps(
        {"email": "test@test.com", "password": "pass", "zip_code": "61554"}
    )
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 400
    assert response["body"] == '"User exists"'


def test_successful_user_creation(mocker):
    """Test 12 | Test that a successful user creation returns a 200 status code and the user's information."""
    mocker.patch("signup.app.get_rds_session")
    mocker.patch("signup.app.create_user")
    mocker.patch(
        "signup.app.get_user",
        return_value=User(
            email="test@test.com", zip_code="61554", first_name=None, last_name=None
        ),
    )
    body = json.dumps(
        {"email": "test123@test.com", "password": "passwd", "zip_code": "61554"}
    )
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    # Simulate and assert the response body structure
    expected_user_info = {
        "email": "test@test.com",
        "first_name": None,
        "last_name": None,
        "zip_code": "61554",
        "bio_info": None,
        "email_verified": None,
        "needs_password_reset": None,
    }

    assert json.loads(response["body"])["user"] == expected_user_info


def test_signup_with_full_user_details(mocker):
    """Test 13 | Test that a successful user creation with full user details returns a 200 status code and the user's information."""
    mocker.patch("signup.app.get_rds_session")
    mocker.patch("signup.app.create_user")
    mocker.patch(
        "signup.app.get_user",
        return_value=User(
            email="test@test.com", zip_code="61554", first_name="bob", last_name=None
        ),
    )
    body = json.dumps(
        {
            "email": "test123@test.com",
            "password": "passwd",
            "zip_code": "61554",
            "first_name": "bob",
        }
    )
    event = {"body": body}

    response = app.lambda_handler(event, None)

    assert response["statusCode"] == 200
    expected_user_info = {
        "email": "test@test.com",
        "first_name": "bob",
        "last_name": None,
        "zip_code": "61554",
        "bio_info": None,
        "email_verified": None,
        "needs_password_reset": None,
    }
    assert json.loads(response["body"])["user"] == expected_user_info


def test_lambda_handler_invalid_json(mocker):
    """Test 14 | Test that invalid JSON returns a 400 status code."""
    mocker.patch("signin.app.get_rds_session")

    apigw_event = {"body": "invalid json"}

    ret = app.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 400
    assert ret["body"] == '"Invalid JSON body."'
