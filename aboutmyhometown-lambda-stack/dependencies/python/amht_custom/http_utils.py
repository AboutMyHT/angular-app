import json


def api_response(return_obj, status_code: int = 200):
    return {
        "statusCode": status_code,
        "body": json.dumps(return_obj),
    }
