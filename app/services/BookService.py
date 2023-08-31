from app.dao.BookDao import BookDao


class BookService:
    def __init__(self, book_dao) -> None:
        self.dao = book_dao

    def get_books_by_title(self, name):
        return self.dao.get_book_by_title_dao(name)

    def construct_book_object(book_str):
        pass
