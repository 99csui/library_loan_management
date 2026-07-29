import unittest
from datetime import datetime
from models.loan import Loan
from models.enums import LoanStatus
from repositories.loan_repository import LoanRepository


class TestLoanRepository(unittest.TestCase):

    def setUp(self):
        self.repository = LoanRepository()
        self.borrowed_at = datetime(2026, 7, 17, 15, 30)
        self.returned_at = datetime(2026, 7, 20, 12, 0)


    def test_new_repository_returns_none_when_loan_does_not_exist(self):
        result = self.repository.get_by_id(1)

        self.assertIsNone(result)

    def test_add_stores_loan_and_get_by_id_returns_it(self):
        loan = Loan(1, 1, 1, self.borrowed_at)
        self.repository.add(loan)
        result = self.repository.get_by_id(loan.id)

        self.assertIs(result, loan)

    def test_get_by_id_returns_none_when_id_does_not_exist(self):
        loan = Loan(1, 1, 1, self.borrowed_at)
        self.repository.add(loan)
        result = self.repository.get_by_id(2)

        self.assertIsNone(result)

    def test_add_raises_type_error_when_value_is_not_loan(self):
        with self.assertRaises(TypeError):
            self.repository.add("text")

    def test_add_raises_value_error_when_loan_id_already_exists(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(1, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        with self.assertRaises(ValueError):
            self.repository.add(loan2)


    def test_list_all_returns_empty_list_when_repository_is_empty(self):
        result = self.repository.list_all()

        self.assertEqual(result,[])

    def test_list_all_returns_all_stored_loans(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)

        result = self.repository.list_all()
        self.assertEqual(result, [loan1, loan2])

    def test_list_all_keeps_insertion_order(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)

        result = self.repository.list_all()

        self.assertIs(result[0], loan1)
        self.assertIs(result[1], loan2)

    def test_list_all_modifying_returned_list_does_not_modify_repository(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)

        modified_list = self.repository.list_all()
        modified_list.clear()

        result = self.repository.list_all()

        self.assertEqual(result, [loan1, loan2])


    def test_list_active_returns_empty_list_when_repository_is_empty(self):
        result = self.repository.list_active()

        self.assertEqual(result,[])

    def test_list_active_returns_empty_list_when_all_loans_are_returned(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 2, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        
        result = self.repository.list_active()

        self.assertEqual(result, [])

    def test_list_active_returns_all_loans_when_all_loans_are_active(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        
        result = self.repository.list_active()

        self.assertEqual(result, [loan1, loan2])

    def test_list_active_returns_only_active_loans_when_loans_are_mixed(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan3 = Loan(3, 3, 3, self.borrowed_at)
        loan4 = Loan(4, 4, 4, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        self.repository.add(loan4)
        
        result = self.repository.list_active()

        self.assertEqual(result, [loan1, loan3])

    def test_list_active_keeps_insertion_order(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan3 = Loan(3, 3, 3, self.borrowed_at)
        loan4 = Loan(4, 4, 4, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        self.repository.add(loan4)
        
        result = self.repository.list_active()
        
        self.assertIs(result[0], loan1)
        self.assertIs(result[1], loan3)

    def test_list_active_modifying_returned_list_does_not_modify_repository(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan3 = Loan(3, 3, 3, self.borrowed_at)
        loan4 = Loan(4, 4, 4, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        self.repository.add(loan4)

        modified_list = self.repository.list_active()
        modified_list.clear()

        result = self.repository.list_active()

        self.assertEqual(result, [loan1, loan3])


    def test_find_active_by_book_id_returns_none_when_repository_is_empty(self):
        result = self.repository.find_active_by_book_id(1)

        self.assertIsNone(result)

    def test_find_active_by_book_id_returns_active_loan_when_book_has_an_active_loan(self):
        loan = Loan(1, 1, 1, self.borrowed_at)
        self.repository.add(loan)
        result = self.repository.find_active_by_book_id(loan.book_id)

        self.assertIs(result, loan)

    def test_find_active_by_book_id_returns_none_when_book_does_not_exist(self):
        loan = Loan(1, 1, 1, self.borrowed_at)
        self.repository.add(loan)
        result = self.repository.find_active_by_book_id(2)

        self.assertIsNone(result)

    def test_find_active_by_book_id_returns_none_when_book_has_only_returned_loans(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 1, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        result = self.repository.find_active_by_book_id(1)

        self.assertIsNone(result)

    def test_find_active_by_book_id_ignores_returned_loans_and_returns_active_loan(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 1, 2, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan3 = Loan(3, 1, 3, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan4 = Loan(4, 1, 4, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        self.repository.add(loan4)
        result = self.repository.find_active_by_book_id(loan4.book_id)

        self.assertIs(result, loan4)

    def test_find_active_by_book_id_returns_none_when_active_loan_belongs_to_another_book(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        result = self.repository.find_active_by_book_id(1)

        self.assertIsNone(result)
        

    def test_find_active_by_member_id_returns_empty_list_when_repository_is_empty(self):
        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result, [])

    def test_find_active_by_member_id_returns_empty_list_when_member_has_no_loans(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 2, 1, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        result = self.repository.find_active_by_member_id(3)

        self.assertEqual(result, [])
        
    def test_find_active_by_member_id_returns_empty_list_when_member_has_only_returned_loans(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 2, 1, self.borrowed_at,  self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result, [])

    def test_find_active_by_member_id_returns_all_active_loans_for_member(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 1, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result, [loan1, loan2])

    def test_find_active_by_member_id_ignores_active_loans_from_other_members(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 2, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result, [loan1])

    def test_find_active_by_member_id_ignores_returned_loans_from_same_member(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at, self.returned_at, LoanStatus.RETURNED)
        loan2 = Loan(2, 2, 1, self.borrowed_at)
        loan3 = Loan(3, 3, 1, self.borrowed_at,  self.returned_at, LoanStatus.RETURNED)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result, [loan2])
        
        
    def test_find_active_by_member_id_preserves_insertion_order(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 1, self.borrowed_at)
        loan3 = Loan(3, 3, 1, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result[0], loan1)
        self.assertEqual(result[1], loan2)
        self.assertEqual(result[2], loan3)

    def test_find_active_by_member_id_modifying_returned_list_does_not_modify_repository(self):
        loan1 = Loan(1, 1, 1, self.borrowed_at)
        loan2 = Loan(2, 2, 1, self.borrowed_at)
        loan3 = Loan(3, 3, 1, self.borrowed_at)
        self.repository.add(loan1)
        self.repository.add(loan2)
        self.repository.add(loan3)
        
        modified_list = self.repository.find_active_by_member_id(1)
        modified_list.clear()

        result = self.repository.find_active_by_member_id(1)

        self.assertEqual(result, [loan1, loan2, loan3])