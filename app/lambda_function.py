import boto3
from app.services.BookService import BookService
import json
from http import HTTPStatus
from aws_lambda_powertools import Logger
from app.models.Response import Response

logger = Logger()
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Book')
book_service = BookService(table)


def lambda_handler(event, context):
    try:
        logger.info(event)
        method = event.get('httpMethod')
        params = event.get('queryStringParameters')
        body = event.get('body')

        if (method == 'GET'):
            return get_books(params)
        if (method == 'POST'):
            return add_book(body)
    except Exception as e:
        logger.error(e)
        return Response(HTTPStatus.INTERNAL_SERVER_ERROR, json.dumps('Error')).__dict__


def get_books(params):
    logger.info('Get Books ', params)
    author = params.get('author')
    title = params.get('title')
    statusCode = HTTPStatus.OK
    result = None
    if (title):
        if (author):
            result = book_service.get_book_by_title_and_author(author, title)
        else:
            result = book_service.get_books_by_title(title)
        statusCode = HTTPStatus.OK
    else:
        statusCode = HTTPStatus.BAD_REQUEST
    return Response(statusCode, json.dumps(result)).__dict__


def add_book(body):
    body = json.loads(body)
    logger.debug("add book", body)
    result = {}
    statusCode = HTTPStatus.OK
    author = body.get('author')
    title = body.get('title')
    publication_date = body.get('publication_date')
    if (author and title and publication_date):
        try:
            book_service.add_book(title, author, publication_date)
        except ValueError:
            statusCode = HTTPStatus.BAD_REQUEST
            result = 'Book Already exists'
        except Exception as e:
            logger.error('Error in adding book', e)
            result = None
            statusCode = HTTPStatus.INTERNAL_SERVER_ERROR
    return Response(statusCode, json.dumps(result)).__dict__
