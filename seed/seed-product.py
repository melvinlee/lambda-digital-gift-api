import csv
import boto3
dynamodb = boto3.resource('dynamodb')


with open('./products.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    table = dynamodb.Table('gift-product-dev')

    with table.batch_writer() as batch:
        for row in reader:
            batch.put_item(Item={
                'id': row['id'],
                'name': row['name'],
                'price': row['price'],
                'score': row['score']
            })
