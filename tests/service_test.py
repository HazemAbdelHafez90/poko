
from unittest import TestCase
import moto
import boto3
from app.dao.BookDao import BookDao
from app.services.BookService import BookService
from app.models.Book import Book


@moto.mock_dynamodb
class TestBookService(TestCase):
    def setUp(self):
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = dynamodb.create_table(
            TableName='Book',
            KeySchema=[{"AttributeName": "author", "KeyType": "HASH"}, {
                "AttributeName": "title", "KeyType": "RANGE"}],
            AttributeDefinitions=[
                {"AttributeName": "author", "AttributeType": "S"}, {"AttributeName": "title", "AttributeType": "S"}],
            BillingMode='PAY_PER_REQUEST',

        )
        self.service = BookService(self.table)

    def test_find_book_by_title_success(self):
        self.table.put_item(Item={"title": "book1", "author": "test"})
        test_return_value = self.service.get_books_by_title('Book1')
        # Test
        self.assertEqual(len(test_return_value), 1)

    def test_find_more_than_one_book_by_title_success(self):
        self.table.put_item(Item={"title": "book1", "author": "test"})
        self.table.put_item(Item={"title": "book2", "author": "test"})
        test_return_value = self.service.get_books_by_title('Book')
        # Test
        self.assertEqual(len(test_return_value), 2)

    def test_find_book_by_title_and_author_success(self):
        book = Book('book1', 'test', 'Publication_date')
        self.table.put_item(Item=book.__dict__)
        test_return_value = self.service.get_book_by_title_and_author(
            'Test', 'book1')
        # Test
        self.assertEqual(test_return_value, book.__dict__)

    def test_add_book(self):
        book = Book('book1', 'author1', 'date')
        self.service.add_book('book1', 'author1', 'date')
        test_return_value = self.table.get_item(
            Key={'title': 'book1', 'author': 'author1'})['Item']
        self.assertEqual(book.__dict__, test_return_value)

    def test_add_book_already_exists(self):
        book = Book('book1', 'author1', 'date')
        self.table.put_item(Item=book.__dict__)
        with self.assertRaises(ValueError):
            self.service.add_book('book1', 'author1', 'date')
