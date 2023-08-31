import boto3
from app.services.BookService import BookService
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Book')
book_service = BookService(table)


def lambda_handler(event, context):
    print(event)
    print(response)
    response = book_service.get_book()

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
