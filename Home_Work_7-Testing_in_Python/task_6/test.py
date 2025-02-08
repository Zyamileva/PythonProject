import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from bank_account import BankAccount
from unittest.mock import Mock
import pytest


@pytest.fixture
def persona_account():  # noqa: F811
    """Provides a BankAccount fixture for testing,
    This fixture creates a BankAccount instance with an initial balance of 1000 for use in test cases.
    """
    return BankAccount(100)


@pytest.mark.parametrize(
    "deposit_amount, expected_balance", [(50, 150), (100, 200), (120, 220)]
)
def test_deposit(persona_account, deposit_amount, expected_balance):
    """Test the deposit method with valid input.
    This test verifies that the deposit method correctly updates the account balance
    when given valid deposit amounts."""
    persona_account.deposit(deposit_amount)
    assert persona_account.get_balance() == expected_balance


def test_deposit_error(persona_account):
    """Test the deposit method for invalid input.
    This test ensures that the deposit method raises a ValueError when attempting to deposit
    a zero or negative amount."""
    with pytest.raises(ValueError, match="Deposit amount must be positive."):
        persona_account.deposit(0)
    with pytest.raises(ValueError, match="Deposit amount must be positive."):
        persona_account.deposit(-10)


@pytest.mark.parametrize(
    "withdrawal_money, exchange_balance", [(100, 0), (50, 50), (10, 90)]
)
def test_withdrawal_money(persona_account, withdrawal_money, exchange_balance):
    """Test the withdrawal method with valid input.
    This test verifies that the withdrawal method correctly updates the account balance
    when given valid withdrawal amounts."""
    persona_account.withdraw(withdrawal_money)
    assert persona_account.get_balance() == exchange_balance


def test_withdrawal_error(persona_account):
    """Test the withdrawal method for invalid input.
    This test ensures that the withdrawal method raises a ValueError when attempting to withdraw
    a zero or negative amount."""
    with pytest.raises(ValueError, match="Withdrawal amount must be positive."):
        persona_account.withdraw(0)
    with pytest.raises(ValueError, match="Withdrawal amount must be positive."):
        persona_account.withdraw(-100)


def test_withdraw_insufficient_funds(persona_account):
    """Test the withdrawal method for insufficient funds.
    This test ensures that the withdrawal method raises an InsufficientFundsError when attempting to withdraw
    more than the current balance."""
    with pytest.raises(ValueError, match="Insufficient funds."):
        persona_account.withdraw(1500)


@pytest.mark.skipif(
    BankAccount(0).get_balance() == 0, reason="Insufficient funds in the account"
)
def test_balance_empty():
    """Test the get_balance method with an empty account.
    This test ensures that the get_balance method returns 0 when the account balance is zero."""
    assert BankAccount(0).get_balance() == 0


def test_mock_check_balance():
    """Test the mock check_balance method.
    This test ensures that the mock check_balance method returns the balance from a mock API."""
    mock_api = Mock()
    mock_api.get_balance.return_value = 700
    assert mock_api.get_balance() == 700
    mock_api.get_balance.assert_called_once()


if __name__ == "__main__":
    pytest.main()
