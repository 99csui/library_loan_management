import unittest
from models.member import Member

class TestMember(unittest.TestCase):

    def test_member_is_created_successfully(self) -> None:
        member = Member(1, "Harry Valen")

        self.assertIsInstance(member,Member)

    def test_member_stores_expected_data(self) -> None:
        member = Member(1, "Harry Valen")

        self.assertEqual(member.id,1)
        self.assertEqual(member.name,"Harry Valen")


    def test_member_raises_type_error_when_id_is_not_int(self) -> None:
        with self.assertRaises(TypeError):
            Member("1", "Harry Valen")

    def test_member_raises_value_error_when_id_is_zero(self) -> None:
        with self.assertRaises(ValueError):
            Member(0, "Harry Valen")

    def test_member_raises_value_error_when_id_is_negative(self) -> None:
        with self.assertRaises(ValueError):
            Member(-5, "Harry Valen")


    def test_member_raises_type_error_when_name_is_not_string(self) -> None:
        with self.assertRaises(TypeError):
            Member(1, 5)

    def test_member_raises_value_error_when_name_is_empty(self) -> None:
        with self.assertRaises(ValueError):
            Member(1, "")

    def test_member_raises_value_error_when_name_contains_only_spaces(self) -> None:
        with self.assertRaises(ValueError):
            Member(1, "    ")


    def test_member_string_representation(self) -> None:
        member = Member(1, "Harry Valen")
        expected = ("Member ID: 1\n"
                           "Name: Harry Valen")

        self.assertEqual(str(member), expected)