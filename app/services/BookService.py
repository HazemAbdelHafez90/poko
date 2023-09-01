from app.dao.BookDao import BookDao
from app.models.Book import Book


class BookService:
    def __init__(self, book_table) -> None:
        self.dao = BookDao(book_table)

    def get_books_by_title(self, name):
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
        if (name):
            return self.dao.get_book_by_title_dao(name)
        else:
            return []
=======
>>>>>>> Stashed changes
        return self.dao.get_book_by_title_dao(name.lower())

    def get_book_by_title_and_author(self, author, title):
        return self.dao.get_book_by_title_and_author_dao(author.lower(), title.lower())

    def list_all_books(self):
        return self.dao.list_all_books_dao()
<<<<<<< Updated upstream
=======
>>>>>>> b9abbe58fdaf60cacc24df3bc18504080db0e80f
>>>>>>> Stashed changes

    def add_book(self, title, author, publication_date):
        book = Book(title.lower(), author.lower(), publication_date.lower())
        self.dao.add_book_dao(book.__dict__)
