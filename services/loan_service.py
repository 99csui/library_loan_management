from datetime import datetime

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

from models.book import Book
from models.member import Member
from models.loan import Loan


class LoanService:
    def __init__(self, book_repository: BookRepository, member_repository: MemberRepository, loan_repository: LoanRepository):
        self._book_repository = book_repository
        self._member_repository = member_repository
        self._loan_repository = loan_repository
        self.MAX_ACTIVE_LOANS_PER_MEMBER = 3

    def borrow_book(self, loan_id: int, book_id: int, member_id: int) -> Loan:
        if not self._book_repository.exists(book_id):
            raise ValueError("book does not exist")
        
        if not self._member_repository.exists(member_id):
            raise ValueError("member does not exist")
        
        if self._loan_repository.find_active_by_book_id(book_id) is not None:
            raise ValueError("cannot borrow a book with an active loan")

        if len(self._loan_repository.find_active_by_member_id(member_id)) >= self.MAX_ACTIVE_LOANS_PER_MEMBER:
            raise ValueError("member has reached the active loan limit")
        
        borrowed_at = datetime.now()
        loan = Loan(loan_id, book_id, member_id, borrowed_at)
        self._loan_repository.add(loan)
        
        return loan

    def return_book(self, loan_id: int):
        loan = self._loan_repository.get_by_id(loan_id)
        if loan is None:
            raise ValueError("the loan does not exist")

        if not loan.is_active():
            raise ValueError("cannot return an already returned loan")
        