from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


class BookDao:
    def __init__(self, table):
        self.book_table = table

    def get_book_by_title_dao(self, name):
<<<<<<< Updated upstream
        result = self.book_table.scan(FilterExpression=Attr(
            'title').begins_with(name), ConsistentRead=True).get('Items')
        return result

    def list_all_books_dao(self):
        result = self.book_table.scan().get('Items')
        return result
=======
<<<<<<< HEAD
        books = self.book_table.scan(
            FilterExpression=Attr('title').contains(name), ConsistentRead=True).get('Items')
        return books
>>>>>>> Stashed changes

=======
        result = self.book_table.scan(FilterExpression=Attr(
            'title').begins_with(name), ConsistentRead=True).get('Items')
        return result

    def list_all_books_dao(self):
        result = self.book_table.scan().get('Items')
        return result

    def get_book_by_title_and_author_dao(self, author, title):
        result = self.book_table.get_item(
            Key={'author': author, 'title': title}).get('Item')
        return result

>>>>>>> b9abbe58fdaf60cacc24df3bc18504080db0e80f
    def add_book_dao(self, book_dict):
        try:
            self.book_table.put_item(
                Item=book_dict,  ConditionExpression='attribute_not_exists(author)')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError('Book Already exists')
            else:
                raise
