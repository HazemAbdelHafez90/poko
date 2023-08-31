from boto3.dynamodb.conditions import Attr


class BookDao:
    def __init__(self, table):
        self.book_table = table

    def get_book_by_title_dao(self, name):
        books = []
        response = self.book_table.scan(
            FilterExpression=Attr('title').begins_with(name), ConsistentRead=True)

        for item in response['Items']:
            books.append(item)

        return books

    def add_book_dao(self, book_dict):
        self.book_table.put_item(Item=book_dict)
