from dataclasses import dataclass


@dataclass
class Book:
    id: str
    name: str

    def vals(self):
        return {"id": self.id, "name": self.name}


@dataclass
class User:
    id: str
    name: str
    surname: str

    def vals(self):
        return {"id": self.id, "name": self.name, "surname": self.surname}


@dataclass
class Borrowed:
    id: str
    user_id: str
    book_id: str

    def vals(self):
        return {"id": self.id, "user_id": self.user_id, "book_id": self.book_id}
