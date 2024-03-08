import json


def valid_response(return_obj, status_code: int = 200):
    return {
        "statusCode": status_code,
        "body": json.dumps(return_obj),
    }


def invalid_response(error_message: str, status_code: int = 400):
    return {
        "statusCode": status_code,
        "body": {"error": error_message},
    }


def response(return_obj, status_code: int = 200):
    if status_code >= 200 and status_code < 300:
        return valid_response(return_obj, status_code)
    elif status_code >= 400 and status_code <= 500:
        return invalid_response(return_obj, status_code)
    else:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "An unknown error occurred."}),
        }
