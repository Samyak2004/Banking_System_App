import streamlit as st

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount}. New balance is {self.balance}."
        else:
            return "Deposit amount must be positive."

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds. Available balance is {self.balance}.")
        elif amount > 0:
            self.balance -= amount
            return f"Withdrew {amount}. New balance is {self.balance}."
        else:
            return "Withdrawal amount must be positive."

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"Account Number: {self.account_number}, Account Holder: {self.account_holder}, Balance: {self.balance}"

class SavingsAccount(Account):
    def __init__(self, account_number, account_holder, initial_balance=0, interest_rate=0.01):
        super().__init__(account_number, account_holder, initial_balance)
        self.interest_rate = interest_rate

    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        return f"Interest calculated: {interest}. New balance after interest: {self.balance}"

class CheckingAccount(Account):
    def __init__(self, account_number, account_holder, initial_balance=0):
        super().__init__(account_number, account_holder, initial_balance)

class Transaction:
    def __init__(self, transaction_id, from_account, to_account, amount):
        self.transaction_id = transaction_id
        self.from_account = from_account
        self.to_account = to_account
        self.amount = amount

    def execute(self):
        try:
            self.from_account.withdraw(self.amount)
            self.to_account.deposit(self.amount)
            return f"Transaction {self.transaction_id} executed successfully."
        except InsufficientFundsError as e:
            return f"Transaction {self.transaction_id} failed: {e}"

# Streamlit app
def main():
    st.title("Banking System")

    accounts = {}

    menu = ["Create Account", "Deposit Money", "Withdraw Money", "Transfer Money", "Calculate Interest (Savings Account)", "Display Account Info", "Exit"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Create Account":
        st.subheader("Create Account")
        account_number = st.text_input("Enter account number")
        account_holder = st.text_input("Enter account holder name")
        account_type = st.selectbox("Enter account type", ["Savings", "Checking"])
        initial_balance = st.number_input("Enter initial balance", min_value=0.0, format="%.2f")

        if account_type == "Savings":
            interest_rate = st.number_input("Enter interest rate (e.g., 0.01 for 1%)", min_value=0.0, format="%.2f")
            if st.button("Create Account"):
                accounts[account_number] = SavingsAccount(account_number, account_holder, initial_balance, interest_rate)
                st.success("Savings account created successfully!")
        elif account_type == "Checking":
            if st.button("Create Account"):
                accounts[account_number] = CheckingAccount(account_number, account_holder, initial_balance)
                st.success("Checking account created successfully!")

    elif choice == "Deposit Money":
        st.subheader("Deposit Money")
        account_number = st.text_input("Enter account number")
        amount = st.number_input("Enter amount to deposit", min_value=0.0, format="%.2f")
        if st.button("Deposit"):
            if account_number in accounts:
                result = accounts[account_number].deposit(amount)
                st.success(result)
            else:
                st.error("Account not found!")

    elif choice == "Withdraw Money":
        st.subheader("Withdraw Money")
        account_number = st.text_input("Enter account number")
        amount = st.number_input("Enter amount to withdraw", min_value=0.0, format="%.2f")
        if st.button("Withdraw"):
            if account_number in accounts:
                try:
                    result = accounts[account_number].withdraw(amount)
                    st.success(result)
                except InsufficientFundsError as e:
                    st.error(e)
            else:
                st.error("Account not found!")

    elif choice == "Transfer Money":
        st.subheader("Transfer Money")
        from_account_number = st.text_input("Enter from account number")
        to_account_number = st.text_input("Enter to account number")
        amount = st.number_input("Enter amount to transfer", min_value=0.0, format="%.2f")
        if st.button("Transfer"):
            if from_account_number in accounts and to_account_number in accounts:
                transaction = Transaction("T001", accounts[from_account_number], accounts[to_account_number], amount)
                result = transaction.execute()
                st.success(result)
            else:
                st.error("One or both accounts not found!")

    elif choice == "Calculate Interest (Savings Account)":
        st.subheader("Calculate Interest (Savings Account)")
        account_number = st.text_input("Enter account number")
        if st.button("Calculate Interest"):
            if account_number in accounts:
                if isinstance(accounts[account_number], SavingsAccount):
                    result = accounts[account_number].calculate_interest()
                    st.success(result)
                else:
                    st.error("Interest calculation is only available for savings accounts!")
            else:
                st.error("Account not found!")

    elif choice == "Display Account Info":
        st.subheader("Display Account Info")
        account_number = st.text_input("Enter account number")
        if st.button("Display Info"):
            if account_number in accounts:
                result = accounts[account_number].display_account_info()
                st.info(result)
            else:
                st.error("Account not found!")

    elif choice == "Exit":
        st.subheader("Exiting the application. Goodbye!")

if __name__ == "__main__":
    main()