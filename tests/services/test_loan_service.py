import unittest
from datetime import datetime

from services.loan_service import LoanService
from services.library_service import LibraryService

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

from models.book import Book
from models.member import Member
from models.loan import Loan
from models.enums import LoanStatus
datetime(2026, 7, 17, 15, 30)

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

    def test_borrow_book_raises_value_error_when_book_has_active_loan(self):
        self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        self.library_service.register_member(1, "Harry Owen")
        loan = Loan(1, 1, 1, datetime(2026, 7, 17, 15, 30))
        self.loan_repository.add(loan)
        with self.assertRaises(ValueError):
            self.service.borrow_book(2, 1, 1)
        self.assertEqual(len(self.loan_repository.list_all()), 1)

    def test_borrow_book_does_not_raise_when_active_loan_belongs_to_another_book(self):
        pass
    
    def test_borrow_book_raises_value_error_when_member_reaches_active_loan_limit(self):
        self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        self.library_service.register_book(2, "Python Crash Course", "Eric Matthes")
        self.library_service.register_book(3, "Code Complete", "Steve McConnell")
        self.library_service.register_book(4, "Designing Data-Intensive Applications", "Martin Kleppmann")
        self.library_service.register_member(1, "Harry Owen")
        loan1 = Loan(1, 1, 1, datetime(2026, 7, 17, 15, 30))
        loan2 = Loan(2, 2, 1, datetime(2026, 7, 17, 15, 30))
        loan3 = Loan(3, 3, 1, datetime(2026, 7, 17, 15, 30))
        self.loan_repository.add(loan1)
        self.loan_repository.add(loan2)
        self.loan_repository.add(loan3)
        with self.assertRaises(ValueError):
            self.service.borrow_book(4, 4, 1)
        self.assertEqual(len(self.loan_repository.list_all()), 3)
    
    def test_borrow_book_returns_created_loan(self):
        book = self.library_service.register_book(1, "Designing Data-Intensive Applications", "Martin Kleppmann")
        member = self.library_service.register_member(1, "Harry Owen")
        registered_loan = self.service.borrow_book(1, book.id, member.id)

        self.assertIsInstance(registered_loan, Loan)
        self.assertEqual(registered_loan.id, 1)
        self.assertEqual(registered_loan.book_id, book.id)
        self.assertEqual(registered_loan.member_id, member.id)

    def test_borrow_book_adds_loan_to_repository(self):
        book = self.library_service.register_book(1, "Designing Data-Intensive Applications", "Martin Kleppmann")
        member = self.library_service.register_member(1, "Harry Owen")
        registered_loan = self.service.borrow_book(1, book.id, member.id)
        stored_loan = self.loan_repository.get_by_id(registered_loan.id)

        self.assertEqual(stored_loan, registered_loan)

    def test_borrow_book_stores_returned_loan_instance(self):
        book = self.library_service.register_book(1, "Designing Data-Intensive Applications", "Martin Kleppmann")
        member = self.library_service.register_member(1, "Harry Owen")
        registered_loan = self.service.borrow_book(1, book.id, member.id)
        stored_loan = self.loan_repository.get_by_id(registered_loan.id)

        self.assertIs(registered_loan, stored_loan)

    def test_borrow_book_creates_active_loan(self):
        book = self.library_service.register_book(1, "Designing Data-Intensive Applications", "Martin Kleppmann")
        member = self.library_service.register_member(1, "Harry Owen")
        registered_loan = self.service.borrow_book(1, book.id, member.id)

        self.assertTrue(registered_loan.is_active())

    def test_borrow_book_sets_current_borrowed_at(self):
        book = self.library_service.register_book(1, "Designing Data-Intensive Applications", "Martin Kleppmann")
        member = self.library_service.register_member(1, "Harry Owen")
        time_before = datetime.now()
        registered_loan = self.service.borrow_book(1, book.id, member.id)
        time_after = datetime.now()
        
        self.assertGreaterEqual(registered_loan.borrowed_at, time_before)
        self.assertLessEqual(registered_loan.borrowed_at, time_after)

    def test_borrow_book_raises_value_error_when_loan_id_already_exists(self):
        book1 = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        book2 = self.library_service.register_book(2, "Python Crash Course", "Eric Matthes")
        member = self.library_service.register_member(1, "Harry Owen")
        registered_loan = self.service.borrow_book(1, book1.id, member.id)
        
        with self.assertRaises(ValueError):
            self.service.borrow_book(1, book2.id, member.id)
        self.assertEqual(len(self.loan_repository.list_active()), 1)

    def test_return_book_raises_value_error_when_loan_does_not_exist(self):
        book = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        member = self.library_service.register_member(1, "Harry Owen")
        loan = self.service.borrow_book(1, book.id, member.id)

        with self.assertRaises(ValueError):
            self.service.return_book(2)
        self.assertEqual(self.loan_repository.list_all(), [loan])

    def test_return_book_raises_value_error_when_loan_is_already_returned(self):
        book = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        member = self.library_service.register_member(1, "Harry Owen")
        loan = Loan(1, 1, 1, datetime(2026, 7, 17, 15, 30), datetime(2026, 7, 17, 15, 30), LoanStatus.RETURNED)
        self.loan_repository.add(loan)

        with self.assertRaises(ValueError):
            self.service.return_book(1)
        self.assertEqual(self.loan_repository.list_all(), [loan])
        self.assertFalse(loan.is_active())

    def test_return_book_returns_returned_loan(self):
        book = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        member = self.library_service.register_member(1, "Harry Owen")
        loan = self.service.borrow_book(1, book.id, member.id)
        self.service.return_book(loan.id)

        self.assertEqual(len(self.loan_repository.list_active()), 0)

    def test_return_book_returns_stored_loan_instance(self):
        book = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        member = self.library_service.register_member(1, "Harry Owen")
        loan = self.service.borrow_book(1, book.id, member.id)
        returned_loan = self.service.return_book(loan.id)

        self.assertIsInstance(returned_loan, Loan)
        self.assertIs(returned_loan, loan)

    def test_return_book_marks_loan_as_returned(self):
        book = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        member = self.library_service.register_member(1, "Harry Owen")
        loan = self.service.borrow_book(1, book.id, member.id)
        returned_loan = self.service.return_book(loan.id)

        self.assertFalse(returned_loan.is_active())
        self.assertEqual(returned_loan.status, LoanStatus.RETURNED)

    def test_return_book_sets_current_returned_at(self):
        book = self.library_service.register_book(1, "Clean Code", "Robert C. Martin")
        member = self.library_service.register_member(1, "Harry Owen")
        loan = self.service.borrow_book(1, book.id, member.id)
        time_before = datetime.now()
        returned_loan = self.service.return_book(loan.id)
        time_after = datetime.now()

        self.assertGreaterEqual(returned_loan.returned_at, time_before)
        self.assertLessEqual(returned_loan.returned_at, time_after)
