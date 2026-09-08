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

    def test_run_registers_member_when_user_selects_register_member(self):
        with patch("builtins.input", side_effect=["2", "1", "Jose Osorio", "0"]) as mocked_input:
            self.console_menu.run()            

            registered_member = self.member_repository.get_by_id(1)
            self.assertIsNotNone(registered_member)
            self.assertEqual(registered_member.id, 1)
            self.assertEqual(registered_member.name, "Jose Osorio")

    def test_register_member_keeps_menu_running_when_input_is_invalid(self):
        with patch("builtins.input", side_effect=["2", "abc", "0"]) as mocked_input:
            self.console_menu.run()

            self.assertEqual(mocked_input.call_count, 3)
            self.assertEqual(self.member_repository.list_all(), [])

    def test_run_removes_book_when_user_selects_remove_book(self):
        with patch("builtins.input", side_effect=["1", "1", "Clean Code", "Robert C. Martin", "3", "1", "0"]):
            self.console_menu.run()

            remove_book = self.book_repository.get_by_id(1)
            self.assertIsNone(remove_book)
            self.assertEqual(self.book_repository.list_all(), [])

    def test_remove_book_keeps_menu_running_when_input_is_invalid(self):
        with patch("builtins.input", side_effect=["1", "1", "Clean Code", "Robert C. Martin", "3", "abc", "0"]) as mocked_input:
            self.console_menu.run()

            remove_book = self.book_repository.get_by_id(1)
            self.assertEqual(mocked_input.call_count, 7)
            self.assertIsNotNone(remove_book)
            self.assertEqual(self.book_repository.list_all(), [remove_book])

    def test_run_removes_member_when_user_selects_remove_member(self):
        with patch("builtins.input", side_effect=["2", "1", "Ignacio Fuentes", "4", "1", "0"]):
            self.console_menu.run()

            remove_member = self.member_repository.get_by_id(1)
            self.assertIsNone(remove_member)
            self.assertEqual(self.member_repository.list_all(), [])

    def test_remove_member_keeps_menu_running_when_input_is_invalid(self):
        with patch("builtins.input", side_effect=["2", "1", "Ignacio Fuentes", "4", "abc", "0"]) as mocked_input:
            self.console_menu.run()

            remove_member = self.member_repository.get_by_id(1)
            self.assertEqual(mocked_input.call_count, 6)
            self.assertIsNotNone(remove_member)
            self.assertEqual(self.member_repository.list_all(), [remove_member])

    def test_run_borrows_book_when_user_selects_borrow_book(self):
        self.library_service.register_book(1, "Clean code", "Robert C. Martin")
        self.library_service.register_member(1, "Harry Owen")

        with patch("builtins.input", side_effect=["5", "1", "1", "1", "0"]):
            self.console_menu.run()

            added_loan = self.loan_repository.get_by_id(1)

            self.assertIsNotNone(added_loan)
            self.assertEqual(added_loan.book_id, 1)
            self.assertEqual(added_loan.member_id, 1)
            self.assertTrue(added_loan.is_active())

    def test_borrow_book_keeps_menu_running_when_input_is_invalid(self):
        self.library_service.register_book(1, "Clean code", "Robert C. Martin")
        self.library_service.register_member(1, "Harry Owen")

        with patch("builtins.input", side_effect=["5", "abc", "0"]) as mocked_input:
            self.console_menu.run()

            self.assertEqual(mocked_input.call_count, 3)
            self.assertEqual(self.loan_repository.list_all(), [])

    def test_run_returns_book_when_user_selects_return_book(self):
        self.library_service.register_book(1, "Clean code", "Robert C. Martin")
        self.library_service.register_member(1, "Harry Owen")
        self.loan_service.borrow_book(1, 1, 1)

        with patch("builtins.input", side_effect=["6", "1", "0"]):
            self.console_menu.run()

            loan = self.loan_repository.get_by_id(1)

            self.assertIsNotNone(loan)
            self.assertFalse(loan.is_active())

    def test_return_book_keeps_menu_running_when_input_is_invalid(self):
        self.library_service.register_book(1, "Clean code", "Robert C. Martin")
        self.library_service.register_member(1, "Harry Owen")
        self.loan_service.borrow_book(1, 1, 1)

        with patch("builtins.input", side_effect=["6", "abc", "0"]) as mocked_input:
            self.console_menu.run()

            loan = self.loan_repository.get_by_id(1)

            self.assertEqual(mocked_input.call_count, 3)
            self.assertTrue(loan.is_active())

    def test_run_lists_books_when_user_selects_list_books(self):
        self.library_service.register_book(1, "Clean code", "Robert C. Martin")
        self.library_service.register_book(2, "Python Crash Course", "Eric Matthes")

        with patch("builtins.input", side_effect=["7", "0"]), patch("builtins.print") as mocked_input:

            self.console_menu.run()

            mocked_input.assert_any_call("1 - Clean code - Robert C. Martin")
            mocked_input.assert_any_call("2 - Python Crash Course - Eric Matthes")

    def test_run_lists_available_books_when_user_selects_list_available_books(self):
        self.library_service.register_book(1, "Clean code", "Robert C. Martin")
        self.library_service.register_book(2, "Python Crash Course", "Eric Matthes")
        self.library_service.register_member(1, "Harry Owen")
        self.loan_service.borrow_book(1, 1, 1)

        with patch("builtins.input", side_effect=["8", "0"]), patch("builtins.print") as mocked_input:
            self.console_menu.run()
            
            mocked_input.assert_any_call("2 - Python Crash Course - Eric Matthes")
