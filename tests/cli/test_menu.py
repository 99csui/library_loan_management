import unittest
from unittest.mock import patch

from cli.console_menu import ConsoleMenu

from services.library_service import LibraryService
from services.loan_service import LoanService

from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository

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