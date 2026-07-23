from models.book import Book

class BookRepository:

    def __init__(self) -> None:
        self._books = []

    def add(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError("cannot add an object that is not an instance of Book")
        
        if self.get_by_id(book.id) is not None:
            raise ValueError("cannot add a book with a duplicated id")
        
        self._books.append(book)


    def get_by_id(self, book_id: int) -> Book | None:
        for book in self._books:
            if book.id == book_id:
                return book
        return None
        

    def exists(self, book_id: int) -> bool:
        return self.get_by_id(book_id) is not None
