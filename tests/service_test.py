
from unittest import TestCase
import moto
import boto3
from app.dao.BookDao import BookDao
from app.services.BookService import BookService


@moto.mock_dynamodb
class TestBookDao(TestCase):
    def setUp(self):
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        self.table = dynamodb.create_table(
            TableName='Book',
            KeySchema=[{"AttributeName": "Author", "KeyType": "HASH"}, {
                "AttributeName": "Title", "KeyType": "RANGE"}],
            AttributeDefinitions=[
                {"AttributeName": "Author", "AttributeType": "S"}, {"AttributeName": "Title", "AttributeType": "S"}],
            BillingMode='PAY_PER_REQUEST',

        )
        self.dao = BookDao(self.table)
        self.service = BookService(self.dao)

    def test_find_book_success(self) -> None:
        self.table.put_item(Item={"Title": "Book1", "Author": "Test"})
        test_return_value = self.service.get_books_by_title('Book1')
        # Test
        self.assertEqual(len(test_return_value), 1)

    def test_find_more_than_one_book_success(self) -> None:
        self.table.put_item(Item={"Title": "Book1", "Author": "Test"})
        self.table.put_item(Item={"Title": "Book2", "Author": "Test"})
        test_return_value = self.service.get_books_by_title('Book')
        # Test
        self.assertEqual(len(test_return_value), 2)
