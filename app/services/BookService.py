from app.dao.BookDao import BookDao
from app.models.Book import Book


class BookService:
    def __init__(self, book_table) -> None:
        self.dao = BookDao(book_table)

    def get_books_by_title(self, name):
        return self.dao.get_book_by_title_dao(name)

    def get_book_by_title_and_author(self, author, title):
        return self.dao.get_book_by_title_and_author_dao(author, title)

    def add_book(self, title, author, publication_date):
        book = Book(title, author, publication_date)
        self.dao.add_book_dao(book.__dict__)
