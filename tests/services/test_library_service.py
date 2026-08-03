import unittest

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository
from services.library_service import LibraryService

from models.book import Book


class TestLibraryService(unittest.TestCase):

    def setUp(self):
        self.book_repository = BookRepository()
        self.member_repository = MemberRepository()
        self.loan_repository = LoanRepository()
        self.service = LibraryService(self.book_repository, self.member_repository, self.loan_repository)
    
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