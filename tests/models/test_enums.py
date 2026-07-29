import unittest
from models.enums import LoanStatus


class TestEnums(unittest.TestCase):

    def test_active_status_has_expected_value(self):
        result = LoanStatus.ACTIVE.value
        
        self.assertEqual(result,"active")
     
    def test_returned_status_has_expected_value(self):
        result = LoanStatus.RETURNED.value
        
        self.assertEqual(result,"returned")


    def test_loan_status_members_are_strings(self):
        result = LoanStatus.ACTIVE
        
        self.assertIsInstance(result,str)
