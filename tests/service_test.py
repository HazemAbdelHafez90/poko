
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
        self.table.put_item(Item={"title": "Book1", "author": "Test"})
        test_return_value = self.service.get_books_by_title('Book1')
        # Test
        self.assertEqual(len(test_return_value), 1)

    def test_find_more_than_one_book_by_title_success(self):
        self.table.put_item(Item={"title": "Book1", "author": "Test"})
        self.table.put_item(Item={"title": "Book2", "author": "Test"})
        test_return_value = self.service.get_books_by_title('Book')
        # Test
        self.assertEqual(len(test_return_value), 2)

    def test_find_book_by_title_and_author_success(self):
        book = Book('Test', 'Book1', 'Publication_date')
        self.table.put_item(Item=book.__dict__)
        test_return_value = self.service.get_book_by_title_and_author(
            'Test', 'Book1')
        # Test
        self.assertEqual(test_return_value, book.__dict__)

    def test_add_book(self):
        book = Book('Book1', 'Author1', 'date')
        self.service.add_book(book.__dict__)
        test_return_value = self.table.get_item(
            Key={'title': 'Book1', 'author': 'Author1'})['Item']
        self.assertEqual(book.__dict__, test_return_value)
