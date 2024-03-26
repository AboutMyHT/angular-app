import json

allowed_origin = "https://www.aboutmyhometown.com"


def api_response(return_obj, status_code: int = 200):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": allowed_origin,
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            # "Access-Control-Allow-Credentials": "true",
        },
        "body": json.dumps(return_obj),
    }
