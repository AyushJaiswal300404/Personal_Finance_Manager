import pandas as pd
from datetime import datetime

# Store transactions in memory
transactions = []

def add_transaction():
    date = input("Enter date (DD-MM-YYYY): ")
    amount = float(input("Enter amount: "))
    category = input("Enter category (Income/Expense): ")
    description = input("Enter description: ")
    
    transaction = {
        "Date": date,
        "Amount": amount,
        "Category": category,
        "Description": description
    }
    transactions.append(transaction)
    print("Transaction added successfully!")

def view_transactions():
    if not transactions:
        print("No transactions found.")
        return
        
    df = pd.DataFrame(transactions)
    print("\nAll Transactions:")
    print(df)
    
    total_income = df[df["Category"] == "Income"]["Amount"].sum()
    total_expense = df[df["Category"] == "Expense"]["Amount"].sum()
    print(f"\nTotal Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Net Balance: {total_income - total_expense}")

def main():
    while True:
        print("\n1. Add Transaction")
        print("2. View Transactions")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            print("Thank you for using Finance Manager!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()