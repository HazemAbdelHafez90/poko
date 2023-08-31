from unittest import TestCase
import moto
import boto3
from app.models.Book import Book
from app.dao.BookDao import BookDao


@moto.mock_dynamodb
class TestBookDao(TestCase):
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

    def test_find_book_success(self):
        self.table.put_item(Item={"title": "Book1", "author": "Test"})
        test_return_value = self.dao.get_book_by_title_dao('Book1')
        # Test
        self.assertEqual(len(test_return_value), 1)

    def test_find_more_than_one_book_success(self):
        self.table.put_item(Item={"title": "Book1", "author": "Test"})
        self.table.put_item(Item={"title": "Book2", "author": "Test"})
        test_return_value = self.dao.get_book_by_title_dao('Book')
        # Test
        self.assertEqual(len(test_return_value), 2)

    def test_cannot_find_book_success(self):
        self.table.put_item(Item={"title": "Book3", "author": "Test"})
        test_return_value = self.dao.get_book_by_title_dao('Book2')
        # Test
        self.assertEqual(len(test_return_value), 0)

    def test_add_book(self):
        book = Book('Book1', 'author1', 'date')
        self.dao.add_book_dao(book.__dict__)
        test_return_value = self.table.get_item(
            Key={'title': 'Book1', 'author': 'author1'})['Item']
        self.assertEqual(book.__dict__, test_return_value)
