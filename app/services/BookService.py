from app.dao.BookDao import BookDao
from app.models.Book import Book


class BookService:
    def __init__(self, book_table) -> None:
        self.dao = BookDao(book_table)

    def get_books_by_title(self, name):
        if (name):
            return self.dao.get_book_by_title_dao(name)
        else:
            return []

    def add_book(self, title, author, publication_date):
        book = Book(title, author, publication_date)
        self.dao.add_book_dao(book.__dict__)
