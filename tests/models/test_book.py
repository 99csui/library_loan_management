import unittest
from models.book import Book

class TestBook(unittest.TestCase):

    def test_book_is_created_successfully(self):
        book = Book(1,"Clean Code","Robert C. Martin")

        self.assertIsInstance(book, Book)

    def test_book_stores_expected_data(self):
        book = Book(1,"Clean Code","Robert C. Martin")

        self.assertEqual(book.id,1)
        self.assertEqual(book.title,"Clean Code")
        self.assertEqual(book.author,"Robert C. Martin")
    
    
    def test_book_raises_type_error_when_id_is_not_int(self):
        with self.assertRaises(TypeError):
            Book("1","Clean Code","Robert C. Martin")

    def test_book_raises_value_error_when_id_is_zero(self):
        with self.assertRaises(ValueError):
            Book(0,"Clean Code","Robert C. Martin")

    def test_book_raises_value_error_when_id_is_negative(self):
        with self.assertRaises(ValueError):
            Book(-1,"Clean Code","Robert C. Martin")
    

    def test_book_raises_type_error_when_title_is_not_string(self):
        with self.assertRaises(TypeError):
            Book(1,1,"Robert C. Martin")

    def test_book_raises_value_error_when_title_is_empty(self):
        with self.assertRaises(ValueError):
            Book(1,"","Robert C. Martin")
        
    def test_book_raises_value_error_when_title_contains_only_spaces(self):
        with self.assertRaises(ValueError):
            Book(1,"   ","Robert C. Martin")
    

    def test_book_raises_type_error_when_author_is_not_string(self):
        with self.assertRaises(TypeError):
            Book(1,"Clean Code",1)

    def test_book_raises_value_error_when_author_is_empty(self):
        with self.assertRaises(ValueError):
            Book(1,"Clean Code","")

    def test_book_raises_value_error_when_author_contains_only_spaces(self):
        with self.assertRaises(ValueError):
            Book(1,"Clean Code","    ")
    

    def test_book_string_representation(self):
        book = Book(1,"Clean Code","Robert C. Martin")
        expected = ("Book ID: 1\n"
                           "Title: Clean Code\n"
                           "Author: Robert C. Martin")

        self.assertEqual(str(book),expected)
