from typing import Protocol, TypedDict, Optional


class User(TypedDict):
    id: int
    name: str
    is_admin: bool


class UserDatabase(Protocol):
    def get_user(self, user_id: int) -> Optional[User]: ...
    def save_user(self, user: User) -> None: ...


class InMemoryUserDB(UserDatabase):
    def __init__(self):
        self.users = {}

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def save_user(self, user: User) -> None:
        self.users[user["id"]] = user


if __name__ == "__main__":
    db = InMemoryUserDB()
    db.save_user({"id": 1, "name": "Alice", "is_admin": False})
    print(db.get_user(1))  # {"id": 1, "name": "Alice", "is_admin": False}
    print(db.get_user(2))  # None
