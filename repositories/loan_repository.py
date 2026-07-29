from models.loan import Loan
from models.enums import LoanStatus


class LoanRepository:
    def __init__(self) -> None:
        self._loans = []

    def add(self, loan: Loan) -> None:
        if not isinstance(loan, Loan):
            raise TypeError("cannot add a object that is not an instance of Loan")
        
        if self.get_by_id(loan.id) is not None:
            raise ValueError("cannot add a loan with a duplicated id")
        
        self._loans.append(loan)

    def get_by_id(self, loan_id: int) -> Loan | None:
        for loan in self._loans:
            if loan.id == loan_id:
                return loan
        return None
    
    def list_all(self) -> list[Loan]:
        return self._loans.copy()
    
    def list_active(self) -> list[Loan]:
        return [loan for loan in self.list_all() if loan.status == LoanStatus.ACTIVE]

    def find_active_by_book_id(self, book_id: int) -> Loan | None:
        active_loans = self.list_active()

        for loan in active_loans:
            if loan.book_id == book_id:
                return loan
        return None
    
    def find_active_by_member_id(self, member_id: int) -> list[Loan]:
        return [loan for loan in self.list_active() if loan.member_id == member_id]

