import unittest

from services.loan_service import LoanService
from services.library_service import LibraryService

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

from models.book import Book
from models.member import Member
from models.loan import Loan
from models.enums import LoanStatus


class TestLoanService(unittest.TestCase):

    def setUp(self):
        self.book_repository = BookRepository()
        self.member_repository = MemberRepository()
        self.loan_repository = LoanRepository()
        self.service = LoanService(self.book_repository, self.member_repository, self.loan_repository)
        self.library_service = LibraryService(self.book_repository, self.member_repository, self.loan_repository)

    def test_loan_service_can_be_created_with_repositories(self):
        self.assertIsInstance(self.service, LoanService)

    def test_loan_service_keeps_book_repository_dependency(self):
        self.assertIs(self.service._book_repository, self.book_repository)

    def test_loan_service_keeps_member_repository_dependency(self):
        self.assertIs(self.service._member_repository, self.member_repository)

    def test_loan_service_keeps_loan_repository_dependency(self):
        self.assertIs(self.service._loan_repository, self.loan_repository)

    def test_borrow_book_raises_value_error_when_book_does_not_exist(self):
        self.library_service.register_member(1, "Harry Owen")
        with self.assertRaises(ValueError):
            self.service.borrow_book(1, 1, 1)
        self.assertEqual(len(self.loan_repository.list_all()), 0)

    def test_borrow_book_raises_value_error_when_member_does_not_exist(self):
        self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        with self.assertRaises(ValueError):
            self.service.borrow_book(1, 1, 1)
        self.assertEqual(len(self.loan_repository.list_all()), 0)
