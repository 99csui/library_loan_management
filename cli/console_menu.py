from services.library_service import LibraryService
from services.loan_service import LoanService

class ConsoleMenu:

    def __init__(self, library_service: LibraryService, loan_service: LoanService) -> None:
        self._library_service = library_service
        self._loan_service = loan_service

    def run(self) -> None:
        running = True
        while running:
            print(self._show_menu())
            get_option = input("Select an option\n").strip()
            if get_option == "0":
                running = False
                print("Goodbye!")

            elif get_option == "1":
                self._register_book()

            elif get_option == "2":
                self._register_member()

            elif get_option == "3":
                self._remove_book()

            elif get_option == "4":
                self._remove_member()

            elif get_option == "5":
                self._borrow_book()

            elif get_option == "6":
                self._return_book()

            elif get_option == "7":
                self._list_books()

            elif get_option == "8":
                self._list_available_books()

            elif get_option == "9":
                self._list_active_loans()

            elif get_option == "10":
                self._find_loans_by_member()

    def _show_menu(self) -> str:
        return (
            "==== Library Loan Management ====\n"
            "1. Register book\n"
            "2. Register member\n"
            "3. Remove book\n"
            "4. Remove member\n"
            "5. Borrow book\n"
            "6. Return book\n"
            "7. List books\n"
            "8. List available books\n"
            "9. List active loans\n"
            "10. Find loans by member\n"
            "0. Exit")

    def _register_book(self) -> None:
        print("*** Register Book ***")

        book_id = self._read_id("id: ")
        if book_id is None:
            return
        
        title = input("title: ").strip()
        author = input("author: ").strip()

        try:
            self._library_service.register_book(book_id, title, author)
            print("Book registered successfully")
        except (TypeError, ValueError) as error:
            print(error)

    def _register_member(self) -> None:
        print("*** Register Member ***")

        member_id = self._read_id("id: ")
        if member_id is None:
            return

        name = input("name: ").strip()

        try:
            self._library_service.register_member(member_id, name)
            print("Member registered successfully")
        except (TypeError, ValueError) as error:
            print(error)

    def _remove_book(self) -> None:
        print("*** Remove Book ***")

        book_id = self._read_id("id: ")
        if book_id is None:
            return

        try:
            self._library_service.remove_book(book_id)
            print("Book removed successfully")
        except (TypeError, ValueError) as error:
            print(error)

    def _remove_member(self) -> None:
        print("*** Remove Member ***")
        
        member_id = self._read_id("id: ")
        if member_id is None:
            return
        
        try:
            self._library_service.remove_member(member_id)
            print("Member removed successfully")
        except (TypeError, ValueError) as error:
            print(error)

    def _borrow_book(self):
        print("*** Borrow Book ***")

        loan_id = self._read_id("loan id: ")
        if loan_id is None:
            return
        book_id = self._read_id("book id: ")
        if book_id is None:
            return
        member_id = self._read_id("member id: ")
        if member_id is None:
            return

        try:
            self._loan_service.borrow_book(loan_id, book_id, member_id)
            print("Loan added successfully")
        except (TypeError, ValueError) as error:
            print(error)

    def _return_book(self) -> None:
        print("*** Return Book ***")

        loan_id = self._read_id("loan id: ")
        if loan_id is None:
            return

        try:
            self._loan_service.return_book(loan_id)
            print("Book has been returned successfully")
        except (TypeError, ValueError) as error:
            print(error)

    def _list_books(self) -> None:
        books = self._library_service.list_books()

        for book in books:
            print(f"{book.id} - {book.title} - {book.author}")

    def _list_available_books(self) -> None:
        books = self._loan_service.list_available_books()

        for book in books:
            print(f"{book.id} - {book.title} - {book.author}")

    def _list_active_loans(self) -> None:
        loans = self._loan_service.list_active_loans()

        for loan in loans:
            print(f"Loan {loan.id} - Book {loan.book_id} - Member {loan.member_id}")

    def _find_loans_by_member(self) -> None:
        member_id = self._read_id("member id: ")
        if member_id is None:
            return

        try:
            loans = self._loan_service.find_loans_by_member(member_id)

            for loan in loans:
                print(f"Loan {loan.id} - Book {loan.book_id} - Member {loan.member_id}")

        except (TypeError, ValueError) as error:
            print(error)


    def _read_id(self, prompt: str) -> int | None:
        input_prompt = input(prompt).strip()
        try:
            output_id = int(input_prompt)

            return output_id
        except ValueError:
            print("id must be a number")
            return None