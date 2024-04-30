import json

from signup import app

from amht_custom.sqla.models.tables import User


def test_signup_missing_parameters(mocker):
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
    mocker.patch("signin.app.get_rds_session")

    apigw_event = {"body": "invalid json"}

    ret = app.lambda_handler(apigw_event, "")

    assert ret["statusCode"] == 400
    assert ret["body"] == '"Invalid JSON body."'
