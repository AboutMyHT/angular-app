"""All tests in this file are for the signin lambda function.

Related requirements:
    - 3.1.0
    - 3.2.x
    - 3.3.x
    - 5.4.0
"""

import json

from signin import app

from amht_custom.sqla.models.tables import User


def test_lambda_handler_valid_credentials(mocker):
    """Test 6 | Test that a valid email and password returns a 200 status code and the user's information and session token."""
    mocker.patch("signin.app.check_password", return_value=True)
    mocker.patch(
        "signin.app.get_user",
        return_value=User(
            email="tester@test.com",
            first_name="Bob",
            last_name="the Builder",
            zip_code="61554",
        ),
    )
    mocker.patch(
        "signin.app.generate_session_token",
        return_value="session_token",
    )
    mocker.patch("signin.app.get_rds_session")

    ret = app.lambda_handler(
        {
            "body": '{ "email": "tester@test.com", "password": "passwd" }',
        },
        "",
    )

    assert ret["statusCode"] == 200
    assert json.loads(ret["body"])["user"]["email"] == "tester@test.com"
    assert json.loads(ret["body"])["session_token"] == "session_token"


def test_lambda_handler_invalid_password(mocker):
    """Test 7 | Test that an invalid password returns a 401 status code."""
    mocker.patch("signin.app.get_rds_session")
    mocker.patch("signin.app.check_password", return_value=False)

    apigw_event = {"body": '{ "email": "tester@test.com", "password": "wrongpasswd" }'}

    ret = app.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 401
    assert ret["body"] == '"Invalid email or password"'


def test_lambda_handler_missing_parameters(mocker):
    """Test 8 | Test that missing email and password parameters returns a 400 status code."""
    mocker.patch("signin.app.get_rds_session")

    apigw_event = {
        "body": "{}"  # Missing email and password parameters
    }

    ret = app.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 400
    assert ret["body"] == '"The email and password parameters are required!"'


def test_lambda_handler_invalid_json(mocker):
    """Test 9 | Test that invalid JSON returns a 400 status code."""
    mocker.patch("signin.app.get_rds_session")

    apigw_event = {"body": "invalid json"}

    ret = app.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 400
    assert ret["body"] == '"Invalid JSON body."'
