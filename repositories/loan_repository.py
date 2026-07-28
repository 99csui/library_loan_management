from models.loan import Loan

class LoanRepository:
    def __init__(self) -> None:
        self.loans = []

    def add(self, loan: Loan) -> None:
        if not isinstance(loan, Loan):
            raise TypeError("cannot add a object that is not an instance of Loan")
        
        if self.get_by_id(loan.id) is not None:
            raise ValueError("cannot add a loan with a duplicated id")
        
        self.loans.append(loan)

    def get_by_id(self, loan_id: int) -> Loan | None:
        for loan in self.loans:
            if loan.id == loan_id:
                return loan
        return None