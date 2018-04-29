import os
import json
import logging
import uuid
import time
import traceback
import boto3

from botocore.exceptions import ClientError
from functions import helper

dynamodb = boto3.resource('dynamodb')

# logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):

    try:
        logger.info(event)
        if event['body'] is None:
            logging.error("Validation Failed, body is null or empty")
            return helper.create_response(400, {'error': 'Validation Failed!, body is null or empty'})

        data = json.loads(event['body'])

        error = []
        if 'user_id' not in data:
            logger.error('user_id is null or empty')
            error.append({'user_id': 'user_id is null or empty'})

        if 'product_id' not in data:
            logger.error('product_id is null or empty')
            error.append({'product_id': 'product_id is null or empty'})

        if 'email' not in data:
            logger.error('email is null or empty')
            error.append({'email': 'email is null or empty'})

        if error:
            return helper.create_response(400, {'error': error})

        table = dynamodb.Table(os.getenv("ORDER_TABLE"))
        timestamp = int(time.time() * 1000)

        item = {
            'id': str(uuid.uuid1()),
            'user_id': data['user_id'],
            'product_id': data['product_id'],
            'email': data['email'],
            'createdAt': timestamp,
            'updatedAt': timestamp,
            'redeemed': False
        }

        table.put_item(Item=item)
        return helper.create_response("200", item)
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
        return helper.create_response(500, {'error': e.response['Error']['Message']})
    except Exception:
        tracebackString = traceback.format_exc()
        logger.error(tracebackString)
        return helper.create_response(500, {'error': "Couldn't create order."})
