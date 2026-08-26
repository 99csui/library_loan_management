import unittest
from unittest.mock import patch

from cli.console_menu import ConsoleMenu

from services.library_service import LibraryService
from services.loan_service import LoanService

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

from models.book import Book

class TestConsoleMenu(unittest.TestCase):
    def setUp(self):
        self.book_repository = BookRepository()
        self.member_repository = MemberRepository()
        self.loan_repository = LoanRepository()
        self.loan_service = LoanService(self.book_repository, self.member_repository, self.loan_repository)
        self.library_service = LibraryService(self.book_repository, self.member_repository, self.loan_repository)
        self.console_menu = ConsoleMenu(self.library_service, self.loan_service)

    def test_console_menu_can_be_created_with_services(self):
        self.assertIsInstance(self.console_menu, ConsoleMenu)

    def test_console_menu_keeps_library_service_dependency(self):
        self.assertIs(self.console_menu._library_service, self.library_service)

    def test_console_menu_keeps_loan_service_dependency(self):
        self.assertIs(self.console_menu._loan_service, self.loan_service)

    def test_run_stops_when_user_selects_exit(self):
        with patch("builtins.input", return_value="0") as mocked_input:
            self.console_menu.run()

            mocked_input.assert_called_once()

    def test_run_continues_after_invalid_option_until_exit(self):
        with patch("builtins.input", side_effect=["99", "0"]) as mocked_input:
            self.console_menu.run()
        
            self.assertEqual(mocked_input.call_count, 2)

    def test_run_registers_book_when_user_selects_register_book(self):
        with patch("builtins.input", side_effect=["1", "1", "Clean Code", "Robert C. Martin", "0"]):
            self.console_menu.run()

            registered_book = self.book_repository.get_by_id(1)
            self.assertIsNotNone(registered_book)
            self.assertEqual(registered_book.id, 1)
            self.assertEqual(registered_book.title, "Clean Code")
            self.assertEqual(registered_book.author, "Robert C. Martin")

    def test_register_book_does_not_store_book_when_id_input_is_invalid(self):
        with patch("builtins.input", side_effect=["1", "abc", "0"]) as mocked_input:
            self.console_menu.run()

            self.assertEqual(mocked_input.call_count, 3)
            self.assertEqual(self.book_repository.list_all(), [])
