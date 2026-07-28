import unittest
from datetime import datetime
from models.loan import Loan
from models.enums import LoanStatus
from repositories.loan_repository import LoanRepository


class TestLoanRepository(unittest.TestCase):

    def setUp(self):
        self.repository = LoanRepository()
        self.borrowed_at = datetime(2026, 7, 17, 15, 30)


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

