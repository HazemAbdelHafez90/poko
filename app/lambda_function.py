import boto3
from app.services.BookService import BookService
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Book')
book_service = BookService(table)


def lambda_handler(event, context):
    response = []
    method = event.get('httpMethod')

    if (method == 'GET'):
        params = event.get('queryStringParameters')
        title = params['title']
        response = book_service.get_books_by_title(title)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }


def get_books(params):
    if(params['author']):
        response = book_service.