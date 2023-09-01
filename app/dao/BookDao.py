from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


class BookDao:
    def __init__(self, table):
        self.book_table = table

    def get_book_by_title_dao(self, name):
        books = self.book_table.scan(
            FilterExpression=Attr('title').contains(name), ConsistentRead=True).get('Items')
        return books

    def add_book_dao(self, book_dict):
        try:
            self.book_table.put_item(
                Item=book_dict,  ConditionExpression='attribute_not_exists(author)')
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                raise ValueError('Book Already exists')
            else:
                raise
