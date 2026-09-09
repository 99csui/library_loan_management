from repositories.book_repository import BookRepository
from repositories.member_repository import MemberRepository
from repositories.loan_repository import LoanRepository
from services.library_service import LibraryService
from services.loan_service import LoanService
from cli.console_menu import ConsoleMenu


def main() -> None:
    book_repository = BookRepository()
    member_repository = MemberRepository()
    loan_repository = LoanRepository()

    library_service = LibraryService(
        book_repository,
        member_repository,
        loan_repository,
    )

    loan_service = LoanService(
        book_repository,
        member_repository,
        loan_repository,
    )

    console_menu = ConsoleMenu(
        library_service,
        loan_service,
    )

    console_menu.run()


if __name__ == "__main__":
    main()