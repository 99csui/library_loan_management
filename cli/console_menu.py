from services.library_service import LibraryService
from services.loan_service import LoanService

class ConsoleMenu:

    def __init__(self, library_service: LibraryService, loan_service: LoanService) -> None:
        self._library_service = library_service
        self._loan_service = loan_service

    def run(self)  -> None:
        running = True
        while running:
            print(self._show_menu())
            get_option = input("Select an option\n").strip()
            if get_option == "0":
                running = False
                print("Goodbye!")
            
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
