import unittest
from datetime import datetime

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository
from services.library_service import LibraryService

from models.book import Book
from models.member import Member
from models.loan import Loan
from models.enums import LoanStatus


class TestLibraryService(unittest.TestCase):

    def setUp(self):
        self.book_repository = BookRepository()
        self.member_repository = MemberRepository()
        self.loan_repository = LoanRepository()
        self.service = LibraryService(self.book_repository, self.member_repository, self.loan_repository)
        self.borrowed_at = datetime(2026, 7, 17, 15, 30)
        self.returned_at = datetime(2026, 7, 20, 12, 0)
    
    def test_library_service_can_be_created_with_repositories(self):
        self.assertIsInstance(self.service, LibraryService)

    def test_library_service_keeps_book_repository_dependency(self):
        self.assertIs(self.service._book_repository, self.book_repository)

    def test_library_service_keeps_member_repository_dependency(self):
        self.assertIs(self.service._member_repository, self.member_repository)

    def test_library_service_keeps_loan_repository_dependency(self):
        self.assertIs(self.service._loan_repository, self.loan_repository)

    def test_register_book_adds_book_to_repository(self):
        stored_book = self.service.register_book(1, "Clean Code", "Robert C. Martin")
        
        self.assertEqual(self.book_repository.get_by_id(1), stored_book)

    def test_register_book_returns_stored_book(self):
        stored_book = self.service.register_book(1, "Clean Code", "Robert C. Martin")

        self.assertIsInstance(stored_book, Book)
        self.assertEqual(stored_book.id, 1)
        self.assertEqual(stored_book.title, "Clean Code")
        self.assertEqual(stored_book.author, "Robert C. Martin")

    def test_register_book_stores_returned_book_instance(self):
        stored_book = self.service.register_book(1, "Clean Code", "Robert C. Martin")
        returned_book = self.book_repository.get_by_id(1)
        
        self.assertIs(stored_book, returned_book)

    def test_register_book_raises_error_for_duplicate_book_id(self):
        self.service.register_book(1, "Clean Code", "Robert C. Martin")
        
        with self.assertRaises(ValueError):
            self.service.register_book(1, "Python Crash Course", "Eric Matthes")
        
        self.assertEqual(len(self.book_repository.list_all()), 1)

    def test_register_member_adds_member_to_repository(self):
        registered_member = self.service.register_member(1, "Harry Owen")
        stored_member = self.member_repository.get_by_id(1)

        self.assertEqual(registered_member, stored_member)

    def test_register_member_returns_registered_member(self):
        registered_member = self.service.register_member(1, "Harry Owen")

        self.assertIsInstance(registered_member, Member)
        self.assertEqual(registered_member.id, 1)
        self.assertEqual(registered_member.name, "Harry Owen")

    def test_register_member_stores_returned_member_instance(self):
        registered_member = self.service.register_member(1, "Harry Owen")
        stored_member = self.member_repository.get_by_id(1)

        self.assertIs(registered_member, stored_member)

    def test_register_member_raises_error_for_duplicate_member_id(self):
        self.service.register_member(1, "Harry Owen")
        
        with self.assertRaises(ValueError):
            self.service.register_member(1, "Fran Osorio")
        
        self.assertEqual(len(self.member_repository.list_all()), 1)

    def test_remove_book_removes_book_when_book_has_no_active_loan(self):
        self.service.register_book(1, "Clean Code", "Robert C. Martin")
        result = self.service.remove_book(1)

        self.assertTrue(result)
        self.assertIsNone(self.book_repository.get_by_id(1))

    def test_remove_book_raises_value_error_when_book_does_not_exist(self):
        self.service.register_book(1, "Clean Code", "Robert C. Martin")

        with self.assertRaises(ValueError):
            self.service.remove_book(2)

    def test_remove_book_raises_value_error_when_book_has_active_loan(self):
        registered_book = self.service.register_book(1, "Clean Code", "Robert C. Martin")
        loan = Loan(1, 1, 1, self.borrowed_at)
        self.loan_repository.add(loan)
        
        with self.assertRaises(ValueError):
            self.service.remove_book(1)
        self.assertIs(self.book_repository.get_by_id(1), registered_book)
    
    def test_remove_book_removes_book_when_book_has_only_returned_loans(self):
        self.service.register_book(1, "Clean Code", "Robert C. Martin")
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 1, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan3 = Loan(3, 1, 3, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan4 = Loan(4, 1, 4, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.loan_repository.add(loan1)
        self.loan_repository.add(loan2)
        self.loan_repository.add(loan3)
        self.loan_repository.add(loan4)

        result = self.service.remove_book(1)

        self.assertTrue(result)
        self.assertIsNone(self.book_repository.get_by_id(1))

    def test_remove_member_removes_member_when_member_has_no_active_loans(self):
        self.service.register_member(1, "Harry Owen")
        result = self.service.remove_member(1)

        self.assertTrue(result)
        self.assertIsNone(self.member_repository.get_by_id(1))

    def test_remove_member_raises_value_error_when_member_does_not_exist(self):
        self.service.register_member(1, "Harry Owen")

        with self.assertRaises(ValueError):
            self.service.remove_member(2)
    
    def test_remove_member_raises_value_error_when_member_has_active_loans(self):
        loan = Loan(1, 1, 1, self.borrowed_at)
        self.loan_repository.add(loan)
        registered_member = self.service.register_member(1, "Harry Owen")

        with self.assertRaises(ValueError):
            self.service.remove_member(1)
        self.assertIs(self.member_repository.get_by_id(1), registered_member)

    def test_remove_member_removes_member_when_member_has_only_returned_loans(self):
        self.service.register_member(1, "Harry Owen")
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 2, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan3 = Loan(3, 3, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan4 = Loan(4, 4, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.loan_repository.add(loan1)
        self.loan_repository.add(loan2)
        self.loan_repository.add(loan3)
        self.loan_repository.add(loan4)

        self.service.remove_member(1)

        self.assertIsNone(self.member_repository.get_by_id(1))