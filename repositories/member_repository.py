from models.member import Member

class MemberRepository:

    def __init__(self):
        self._members = []
    
    def add(self, member: Member) -> None:
        if not isinstance(member, Member):
            raise TypeError("cannot add an object that is not an instance of Book")
        
        if self.get_by_id(member.id) is not None:
            raise ValueError("cannot add a book with a duplicated id")
        
        self._members.append(member)

    def get_by_id(self, member_id: int) -> Member | None:
        for member in self._members:
            if member.id == member_id:
                return member
        return None 

