class UserManager:
    """Manages users with their names and ages.
    Provides methods to add, remove, and retrieve users.
    """

    def __init__(self):
        self.users = {}

    def add_user(self, name: str, age: int):
        """Adds a new user.
        Adds a new user with the given name and age to the user manager.
        """
        if age < 0:
            raise ValueError("Age cannot be negative")
        if len(name) < 3:
            raise ValueError("")
        if name in self.users:
            raise ValueError("User already exists")
        self.users[name] = age

    def remove_user(self, name: str):
        """Removes a user.
        Removes the user with the given name from the user manager.
        """
        if name not in self.users:
            raise ValueError("User does not exist")
        del self.users[name]

    def get_all_users(self) -> list:
        """Returns all users.
        Returns a list of all users in the user manager.
        """
        return list(self.users.items())
