class BankAccount:
    """A class representing a simple bank account.
    This class allows users to deposit and withdraw money, as well as check their current balance.
    """

    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount: float):
        """Deposits money into the account.
        This method increases the account balance by the given amount.
        """
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount

    def withdraw(self, amount: float):
        """Withdraws money from the account.
        This method decreases the account balance by the given amount if sufficient funds are available.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance - amount < 0:
            raise ValueError("Insufficient funds.")
        self.balance -= amount

    def get_balance(self) -> float:
        """Returns the current balance of the account.
        This method provides the current account balance.
        """
        return self.balance
