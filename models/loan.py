from dataclasses import dataclass
from models.enums import LoanStatus
from datetime import datetime

@dataclass
class Loan:
    id: int
    book_id: int
    member_id: int
    borrowed_at: datetime
    returned_at: datetime | None = None
    status: LoanStatus = LoanStatus.ACTIVE


    def __post_init__(self) -> None:
        self._validate_positive_integer(self.id, "id")
        self._validate_positive_integer(self.book_id, "book_id")
        self._validate_positive_integer(self.member_id, "member_id")
        self._validate_borrowed_at()
        self._validate_returned_at()
        self._validate_status()
        self._validate_state_consistency()
    
    def __str__(self):
        return (f"id={self.id}\n"
                f"book_id={self.book_id}\n"
                f"member_id={self.member_id}\n"
                f"borrowed_at={self.borrowed_at}\n"
                f"returned_at={self.returned_at}\n"
                f"status={self.status}")

    def _validate_positive_integer(self,value: int, field_name: str) -> None:
        if not isinstance(value, int):
            raise TypeError("id must be an integer.")

        if value <= 0:
            raise ValueError("id must be greater than zero.")
        

    def _validate_borrowed_at(self) -> None:
        if not isinstance(self.borrowed_at, datetime):
            raise TypeError("borrowed_at must be a datetime.")

    def _validate_returned_at(self) -> None:
        if not isinstance(self.returned_at, datetime) and self.returned_at is not None:
            raise TypeError("returned_at must be a None or datetime value.")

    def _validate_status(self) -> None:
        if not isinstance(self.status, LoanStatus):
            raise TypeError("status must be a LoanStatus.")

    def _validate_state_consistency(self) -> None:
        if self.returned_at is not None:
            if self.returned_at < self.borrowed_at:
                raise ValueError("a returned date cannot precede a borrowed date")
            
            if self.status == LoanStatus.ACTIVE:
                raise ValueError("an active loan cannot have a returned date")
        
        if self.status == LoanStatus.RETURNED and self.returned_at is None:
            raise ValueError("a returned loan must have a returned date")
        

    def is_active(self) -> bool:
        return self.status == LoanStatus.ACTIVE
    

    def return_loan(self, returned_at):
        if not self.is_active():
            raise ValueError("cannot return an already returned loan")
    
        if not isinstance(returned_at, datetime):
            raise TypeError("a returned date must be a datetime")

        if returned_at < self.borrowed_at:
            raise ValueError("a returned date cannot precede a borrowed date")     

        self.returned_at = returned_at
        self.status = LoanStatus.RETURNED
