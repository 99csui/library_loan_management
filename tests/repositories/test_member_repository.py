import unittest
from models.member import Member
from repositories.member_repository import MemberRepository

class TestMemberRepository(unittest.TestCase):
    
    def setUp(self):
        self.repository = MemberRepository()

    def test_new_repository_returns_none_when_member_does_not_exist(self):
        result = self.repository.get_by_id(1)

        self.assertIsNone(result)

    def test_add_stores_member_and_get_by_id_returns_it(self):
        member = Member(1, "Harry Leving")
        self.repository.add(member)
        result = self.repository.get_by_id(member.id)

        self.assertIs(result, member)

    def test_get_by_id_returns_none_when_id_does_not_exist(self):
        member = Member(1, "Harry Leving")
        self.repository.add(member)
        result = self.repository.get_by_id(2)

        self.assertIsNone(result)

    def test_add_raises_type_error_when_value_is_not_member(self):
        with self.assertRaises(TypeError):
            self.repository.add("text")

    def test_add_raises_value_error_when_book_id_already_exists(self):
        member1 = Member(1, "Harry Leving")
        member2 = Member(1, "Francisca Osorio")
        self.repository.add(member1)
        with self.assertRaises(ValueError):
            self.repository.add(member2)


    def test_exists_returns_true_when_member_exists(self):
        member = Member(1, "Harry Leving")
        self.repository.add(member)
        result = self.repository.exists(member.id)

        self.assertTrue(result)

    def test_exists_returns_false_when_member_not_exist(self):
        member = Member(1, "Harry Leving")
        self.repository.add(member)
        result = self.repository.exists(2)

        self.assertFalse(result)
    
    def test_exists_returns_false_when_repository_is_empty(self):
        result = self.repository.exists(1)

        self.assertFalse(result)


    def test_list_all_returns_empty_list_when_repository_is_empty(self):
        result = self.repository.list_all()

        self.assertEqual(result,[])

    def test_list_all_returns_all_stored_members(self):
        member1 = Member(1, "Harry Leving")
        member2 = Member(2, "Francisca Osorio")
        self.repository.add(member1)
        self.repository.add(member2)

        result = self.repository.list_all()
        self.assertEqual(result, [member1, member2])

    def test_list_all_keeps_insertion_order(self):
        member1 = Member(1, "Harry Leving")
        member2 = Member(2, "Francisca Osorio")
        self.repository.add(member1)
        self.repository.add(member2)

        result = self.repository.list_all()

        self.assertIs(result[0], member1)
        self.assertIs(result[1], member2)

    def test_list_all_modifying_returned_list_does_not_modify_repository(self):
        member1 = Member(1, "Harry Leving")
        member2 = Member(2, "Francisca Osorio")
        self.repository.add(member1)
        self.repository.add(member2)

        modified_list = self.repository.list_all()
        modified_list.clear()

        result = self.repository.list_all()

        self.assertEqual(result, [member1, member2])
