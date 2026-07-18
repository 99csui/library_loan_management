from dataclasses import dataclass

@dataclass
class Member:
    id: int
    name: str

    def __str__(self) -> str:
        return (f"Member ID: {self.id}\n"
                f"Name: {self.name}")

    def __post_init__(self) -> None:
        self._validate_id()
        self._validate_non_empty_string(self.name, "name")

    def _validate_id(self) -> None:
        if not isinstance(self.id, int):
            raise TypeError("id must be an integer.")

        if self.id <= 0:
            raise ValueError("id must be greater than zero.")
        
    def _validate_non_empty_string(self, value: str, field_name: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")
    
    