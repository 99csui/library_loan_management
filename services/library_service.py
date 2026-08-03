from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

from models.book import Book
from models.member import Member


class LibraryService:
    def __init__(self, book_repository: BookRepository, member_repository: MemberRepository, loan_repository: LoanRepository):
        self._book_repository = book_repository
        self._member_repository = member_repository
        self._loan_repository = loan_repository
    
    def register_book(self, book_id: int, title: str, author: str) -> Book:
        book = Book(book_id, title, author)
        self._book_repository.add(book)
        return book

    def register_member(self, member_id: int, name: str) -> Member:
        member = Member(member_id, name)
        self._member_repository.add(member)
        return member
    
    def remove_book(self, book_id: int) -> bool:
        stored_book = self._book_repository.get_by_id(book_id)
        if stored_book is None:
            raise ValueError("book does not exist")
        
        is_active = self._loan_repository.find_active_by_book_id(book_id)
        if is_active is not None:
            raise ValueError("cannot remove a book with an active loan")
        
        result = self._book_repository.remove(book_id)
        return result
    
    def remove_member(self, member_id: int) -> bool:
        stored_member = self._member_repository.get_by_id(member_id)
        if stored_member is None:
            raise ValueError("member does not exist")
        
        has_active_loans = self._loan_repository.find_active_by_member_id(member_id)
        if len(has_active_loans) > 0:
            raise ValueError("cannot remove member with active loans")

        result = self._member_repository.remove(member_id)        
        return result
        