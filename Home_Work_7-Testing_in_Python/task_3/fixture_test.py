import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from userManager import UserManager


@pytest.fixture()
def user_manager():
    """Provides a UserManager fixture.

    Creates a UserManager instance with two pre-added users, Alice and Bob.
    """

    user = UserManager()
    user.add_user("Alice", 30)
    user.add_user("Bob", 25)
    return user


def test_add_user(user_manager):
    """Tests the add_user method.
    Verifies that adding a user correctly adds the user to the UserManager.
    """
    user_manager.add_user("Lena", 37)
    assert ("Lena", 37) in user_manager.get_all_users()


# 🔹
def test_add_user_duplicate(user_manager):
    """Tests the add_user method.
    Verifies that adding a user correctly adds the user to the UserManager.
    """
    with pytest.raises(ValueError, match="User already exists"):
        user_manager.add_user("Alice", 30)


def test_add_user_negative_age(user_manager):
    """Verifies that adding a user correctly adds the user to the UserManager."""
    with pytest.raises(ValueError, match="Age cannot be negative"):
        user_manager.add_user("David", -5)


def test_remove_user(user_manager):
    """Tests the remove_user method.
    Verifies that removing a user correctly removes them from the UserManager.
    """
    user_manager.remove_user("Alice")
    assert ("Alice", 30) not in user_manager.get_all_users()


def test_remove_user_not_existing(user_manager):
    """Tests removing a non-existing user.
    Verifies that attempting to remove a user that doesn't exist raises a ValueError.
    """
    with pytest.raises(ValueError, match="User does not exist"):
        user_manager.remove_user("Eve")


def test_get_all_users(user_manager):
    """Tests the get_all_users method.
    Verifies that the method returns the correct list of users.
    """
    users = user_manager.get_all_users()
    assert len(users) == 2
    assert ("Alice", 30) in users
    assert ("Bob", 25) in users


def test_requires_three_users(user_manager):
    if len(user_manager.get_all_users()) < 3:
        pytest.skip("Not enough users for the test")
    assert len(user_manager.get_all_users()) >= 3
