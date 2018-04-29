import os
import json
import logging
import boto3
dynamodb = boto3.resource('dynamodb')

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

table_name = os.getenv("PRODUCT_TABLE")


def handler(event, context):
    try:
        table = dynamodb.Table(table_name)
        response = table.scan()
        return build_response(200, response['Items'])
    except Exception as error:
        return build_response(500, logger.error(error))


def build_response(status_code, body=None):
    if body:
        return {'statusCode': status_code, 'body': json.dumps(body)}
    return {'statusCode': status_code}
