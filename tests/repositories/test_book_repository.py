import unittest
from models.book import Book
from repositories.book_repository import BookRepository

class TestBookRepository(unittest.TestCase):
    def setUp(self):
        self.repository = BookRepository()
        
    def test_new_repository_returns_none_when_book_does_not_exist(self):
        result = self.repository.get_by_id(1)

        self.assertIsNone(result)

    def test_add_stores_book_and_get_by_id_returns_it(self):
        book = Book(1, "Clean Code", "Robert C. Martin")
        self.repository.add(book)
        result = self.repository.get_by_id(book.id)

        self.assertIs(result, book)

    def test_get_by_id_returns_none_when_id_does_not_exist(self):
        book = Book(1, "Clean Code", "Robert C. Martin")
        self.repository.add(book)
        result = self.repository.get_by_id(2)

        self.assertIsNone(result)

    def test_add_raises_type_error_when_value_is_not_book(self):
        with self.assertRaises(TypeError):
            self.repository.add("text")

    def test_add_raises_value_error_when_book_id_already_exists(self):
        book1 = Book(1, "Clean Code", "Robert C. Martin")
        book2 = Book(1, "Python Crash Course", "Eric Matthes")
        self.repository.add(book1)
        with self.assertRaises(ValueError):
            self.repository.add(book2)


    def test_exists_returns_true_when_book_exists(self):
        book = Book(1, "Clean Code", "Robert C. Martin")
        self.repository.add(book)
        result = self.repository.exists(book.id)

        self.assertTrue(result)

    def test_exists_returns_false_when_book_not_exist(self):
        book = Book(1, "Clean Code", "Robert C. Martin")
        self.repository.add(book)
        result = self.repository.exists(2)

        self.assertFalse(result)
    
    def test_exists_returns_false_when_repository_is_empty(self):
        result = self.repository.exists(1)

        self.assertFalse(result)


    def test_list_all_returns_empty_list_when_repository_is_empty(self):
        result = self.repository.list_all()

        self.assertEqual(result,[])

    def test_list_all_returns_all_stored_books(self):
        book1 = Book(1, "Clean Code", "Robert C. Martin")
        book2 = Book(2, "Python Crash Course", "Eric Matthes")
        self.repository.add(book1)
        self.repository.add(book2)

        result = self.repository.list_all()
        self.assertEqual(result, [book1, book2])

    def test_list_all_keeps_insertion_order(self):
        book1 = Book(1, "Clean Code", "Robert C. Martin")
        book2 = Book(2, "Python Crash Course", "Eric Matthes")
        self.repository.add(book1)
        self.repository.add(book2)

        result = self.repository.list_all()

        self.assertIs(result[0],book1)
        self.assertIs(result[1],book2)

    def test_list_all_modifying_returned_list_does_not_modify_repository(self):
        book1 = Book(1, "Clean Code", "Robert C. Martin")
        book2 = Book(2, "Python Crash Course", "Eric Matthes")
        self.repository.add(book1)
        self.repository.add(book2)

        modified_list = self.repository.list_all()
        modified_list.clear()

        result = self.repository.list_all()

        self.assertEqual(result, [book1, book2])