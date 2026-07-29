import unittest
from models.loan import Loan
from models.enums import LoanStatus
from datetime import datetime


class TestLoan(unittest.TestCase):

    def test_loan_is_created_successfully(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        loan = Loan(1, 1, 1, borrowed_at)
        
        self.assertIsInstance(loan, Loan)

    def test_loan_stores_expected_data(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        loan = Loan(1, 1, 1, borrowed_at)

        self.assertEqual(loan.id, 1)
        self.assertEqual(loan.book_id, 1)
        self.assertEqual(loan.member_id, 1)
        self.assertEqual(loan.borrowed_at, borrowed_at)
        self.assertIsNone(loan.returned_at)
        self.assertEqual(loan.status, LoanStatus.ACTIVE)

    def test_loan_is_active_by_default(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        loan = Loan(1, 1, 1, borrowed_at)

        result = loan.is_active()
        self.assertTrue(result)

    def test_loan_can_be_created_as_returned(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 20, 12, 0)
        loan = Loan(1, 1, 1, borrowed_at, returned_at, LoanStatus.RETURNED)

        self.assertEqual(loan.returned_at, returned_at)
        self.assertFalse(loan.is_active())

    def test_loan_raises_type_error_when_id_is_not_int(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(TypeError):
            Loan("5", 1, 1, borrowed_at)

    def test_loan_raises_value_error_when_id_is_not_positive(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(ValueError):
            Loan(-2, 1, 1, borrowed_at)

    def test_loan_raises_type_error_when_book_id_is_not_int(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(TypeError):            
            Loan(1, "2", 1, borrowed_at)

    def test_loan_raises_value_error_when_book_id_is_not_positive(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(ValueError):
            Loan(1, -2, 1, borrowed_at)

    def test_loan_raises_type_error_when_member_id_is_not_int(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(TypeError):
            Loan(1, 1, "1", borrowed_at)

    def test_loan_raises_value_error_when_member_id_is_not_positive(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(ValueError):
            Loan(1, 1, -2, borrowed_at)


    def test_loan_raises_type_error_when_borrowed_at_is_not_datetime(self):
        borrowed_at = "2026-07-17"

        with self.assertRaises(TypeError):
            Loan(1, 1, 1, borrowed_at)

    def test_loan_raises_type_error_when_returned_at_is_not_datetime_or_none(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(TypeError):
            Loan(1, 1, 1, borrowed_at, "2026-07-20", LoanStatus.RETURNED)   

    def test_loan_raises_type_error_when_status_is_not_loan_status(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 19, 17, 30)

        with self.assertRaises(TypeError):
            Loan(1, 1, 1, borrowed_at, returned_at, "text")

    def test_loan_raises_value_error_when_returned_at_precedes_borrowed_at(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 13, 13, 30)

        with self.assertRaises(ValueError):
            Loan(1, 1, 1, borrowed_at, returned_at, LoanStatus.RETURNED)

    def test_loan_rejects_active_status_with_returned_at(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 19, 17, 30)

        with self.assertRaises(ValueError):
            Loan(1, 1, 1, borrowed_at, returned_at, LoanStatus.ACTIVE)

    def test_loan_rejects_returned_status_without_returned_at(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)

        with self.assertRaises(ValueError):
            Loan(1, 1, 1, borrowed_at, None, LoanStatus.RETURNED)


    def test_return_loan_changes_status_to_returned(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 20, 12, 0)
        loan = Loan(1, 1, 1, borrowed_at)

        loan.return_loan(returned_at)

        self.assertEqual(loan.status, LoanStatus.RETURNED)

    def test_return_loan_stores_returned_at(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 20, 12, 0)
        loan = Loan(1, 1, 1, borrowed_at)
        loan.return_loan(returned_at)

        self.assertEqual(loan.returned_at, returned_at)

    def test_return_loan_makes_loan_inactive(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 20, 12, 0)
        loan = Loan(1, 1, 1, borrowed_at)
        loan.return_loan(returned_at)

        self.assertFalse(loan.is_active())

    def test_return_loan_raises_type_error_when_date_is_not_datetime(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = "Text"
        loan = Loan(1, 1, 1, borrowed_at)

        with self.assertRaises(TypeError):
            loan.return_loan(returned_at)

    def test_return_loan_raises_value_error_when_date_precedes_borrowed_at(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 10, 12, 0)
        loan = Loan(1, 1, 1, borrowed_at)

        with self.assertRaises(ValueError):
            loan.return_loan(returned_at)

    def test_return_loan_raises_value_error_when_loan_is_already_returned(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        first_returned_at = datetime(2026, 7, 20, 12, 0)
        second_returned_at = datetime(2026, 7, 22, 12, 0)
        loan = Loan(1, 1, 1, borrowed_at)
        loan.return_loan(first_returned_at)

        with self.assertRaises(ValueError):
            loan.return_loan(second_returned_at)



    def test_active_loan_string_representation(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)       
        loan = Loan(1, 1, 1, borrowed_at)

        expected = ("id=1\n"
                "book_id=1\n"
                "member_id=1\n"
                f"borrowed_at={borrowed_at}\n"
                f"returned_at={None}\n"
                f"status={LoanStatus.ACTIVE}")

        self.assertEqual(str(loan), expected)    

    def test_returned_loan_string_representation(self):
        borrowed_at = datetime(2026, 7, 17, 15, 30)
        returned_at = datetime(2026, 7, 20, 12, 0)       
        loan = Loan(1, 1, 1, borrowed_at)
        loan.return_loan(returned_at)
        expected = ("id=1\n"
                "book_id=1\n"
                "member_id=1\n"
                f"borrowed_at={borrowed_at}\n"
                f"returned_at={returned_at}\n"
                f"status={LoanStatus.RETURNED}")

        self.assertEqual(str(loan), expected)
