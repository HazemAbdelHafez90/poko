from unittest import TestCase
import moto
import boto3
from app.models.Book import Book
from app.dao.BookDao import BookDao
import json
from http import HTTPStatus
import app.lambda_function as handler


@moto.mock_dynamodb
class TestHandler(TestCase):
    def setUp(self):
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = dynamodb.create_table(
            TableName='Book',
            KeySchema=[{"AttributeName": "author", "KeyType": "HASH"}, {
                "AttributeName": "title", "KeyType": "RANGE"}],
            AttributeDefinitions=[
                {"AttributeName": "author", "AttributeType": "S"},
                {"AttributeName": "title", "AttributeType": "S"}],
            BillingMode='PAY_PER_REQUEST',

        )
        self.dao = BookDao(self.table)

    def test_find_book_request_success(self):
        self.table.put_item(Item={"title": "Book1", "author": "Test"})
        event = {
            "httpMethod": "GET",
            "headers": {
                "accept": "text/html",
                "accept-encoding": "gzip, deflate, br",
                "Host": "xxx.us-east-2.amazonaws.com",
                "User-Agent": "Mozilla/5.0"
            }, "queryStringParameters": {
                "title": 'Book1'
            },
        }
        response = handler.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(len(json.loads(response['body'])), 1)

    def test_find_multiple_books_request_success(self):
        self.table.put_item(Item={"title": "Book1", "author": "Test"})
        self.table.put_item(Item={"title": "Book2", "author": "Test"})

        event = {
            "httpMethod": "GET",
            "headers": {
                "accept": "text/html",
                "accept-encoding": "gzip, deflate, br",
                "Host": "xxx.us-east-2.amazonaws.com",
                "User-Agent": "Mozilla/5.0"
            }, "queryStringParameters": {
                "title": 'Book'
            },
        }
        response = handler.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(len(json.loads(response['body'])), 2)

    def test_add_book_request_success(self):

        event = {
            "httpMethod": "POST",
            "headers": {
                "accept": "text/html",
                "accept-encoding": "gzip, deflate, br",
                "Host": "xxx.us-east-2.amazonaws.com",
                "User-Agent": "Mozilla/5.0"
            }, "body": "{\n    \"title\": \"book1\",\n    \"author\": \"author1\",\n    \"publication_date\": \"date2\"\n}",
        }
        response = handler.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], 200)

    def test_find_multiple_books_request_failure(self):

        event = {
            "httpMethod": "GET",
            "headers": {
                "accept": "text/html",
                "accept-encoding": "gzip, deflate, br",
                "Host": "xxx.us-east-2.amazonaws.com",
                "User-Agent": "Mozilla/5.0"
            }, "queryStringParameters": {
                "": 'Book'
            },
        }
        response = handler.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], HTTPStatus.BAD_REQUEST)

    def test_add_book_request_missing_parameters(self):

        event = {
            "httpMethod": "POST",
            "headers": {
                "accept": "text/html",
                "accept-encoding": "gzip, deflate, br",
                "Host": "xxx.us-east-2.amazonaws.com",
                "User-Agent": "Mozilla/5.0"
            }, "queryStringParameters": {
                "": 'Book'
            }, "body": "{\n    \"\": \"book1\",\n    \"author\": \"author1\",\n    \"publication_date\": \"date2\"\n}",

        }
        response = handler.lambda_handler(event, None)
        self.assertEqual(response['statusCode'], HTTPStatus.BAD_REQUEST)
        self.assertEqual("Something worng with the paramters",
                         json.loads(response['body']))
