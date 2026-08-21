from cli.console_menu import ConsoleMenu

from services.library_service import LibraryService
from services.loan_service import LoanService


def main() -> None:
    menu = ConsoleMenu(LibraryService(), LoanService())
    menu.run()

if __name__ == "__main__":
    main()