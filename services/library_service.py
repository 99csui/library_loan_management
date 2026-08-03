from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

from models.book import Book


class LibraryService:
    def __init__(self, book_repository: BookRepository, member_repository: MemberRepository, loan_repository: LoanRepository):
        self._book_repository = book_repository
        self._member_repository = member_repository
        self._loan_repository = loan_repository
    
    def register_book(self, book_id: int, title: str, author: str) -> Book:
        book = Book(book_id, title, author)
        self._book_repository.add(book)
        return book

