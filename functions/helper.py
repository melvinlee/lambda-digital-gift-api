import json


def create_response(status_code, body=None):
    if body:
        return {'statusCode': status_code, 'body': json.dumps(body)}
    return {'statusCode': status_code}
