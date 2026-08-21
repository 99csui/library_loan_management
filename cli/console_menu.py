from services.library_service import LibraryService
from services.loan_service import LoanService

class ConsoleMenu:

    def __init__(self, library_service: LibraryService, loan_service: LoanService) -> None:
        self._library_service = library_service
        self._loan_service = loan_service
        
        

    