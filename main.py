import csv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from data_entry import get_date, get_amount, get_category, get_description
from flask import Flask, request, jsonify

class CSV:
    CSV_FILE = "your_csv_file.csv"
    COLUMNS = ["Date", "Amount", "Category", "Description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        with open(cls.CSV_FILE, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transcation(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df.columns = [col.strip().lower() for col in df.columns]  # Normalize column names
        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT)
        start_date = datetime.strptime(start_date, cls.FORMAT)
        end_date = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found.")
        else:
            print(f"Transactions from {start_date.strftime(cls.FORMAT)} to {end_date.strftime(cls.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters={"date": lambda x: x.strftime(cls.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            net_savings = total_income - total_expense
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Net Savings: {net_savings:.2f}")

        return filtered_df

def plot_transactions(df):
    df.set_index('date', inplace=True)
    income_df = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()

def add():
    date = get_date("Enter the date of the transaction(dd-mm-yyyy) or hit 'Enter' for today: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, this is your finance manager app!"

@app.route('/add', methods=['POST'])
def add_entry():
    try:
        data = request.json
        date = data.get('date')
        amount = data.get('amount')
        category = data.get('category')
        description = data.get('description')
        CSV.add_entry(date, amount, category, description)
        return jsonify({"message": "Entry added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def main():
    CSV.initialize_csv()  # Ensure CSV file is initialized
    while True:
        print("1. Add a new transaction")
        print("2. View transactions")
        print("3. Exit")
        choice = input("Enter your choice(1-3): ")
        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date(dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            filtered_df = CSV.get_transcation(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transactions(filtered_df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

if __name__ == "__main__":
    app.run(debug=True)
    main()
