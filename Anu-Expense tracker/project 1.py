import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    amount REAL,
    category TEXT
)
""")


def add_expense():

    title = input("Enter Expense Title: ")

    amount = float(input("Enter Amount: "))

    category = input("Enter Category: ")

    cursor.execute(
        "INSERT INTO expenses (title, amount, category) VALUES (?, ?, ?)",
        (title, amount, category)
    )

    conn.commit()

    print("Expense Added Successfully!")

def view_expenses():

    cursor.execute("SELECT * FROM expenses")

    rows = cursor.fetchall()

    print("\n===== EXPENSE LIST =====")

    for row in rows:
        print(row)

def total_expense():

    cursor.execute("SELECT SUM(amount) FROM expenses")

    total = cursor.fetchone()[0]

    print("\nTotal Expense =", total)

def show_chart():

    cursor.execute("""
    SELECT category, SUM(amount)
    FROM expenses
    GROUP BY category
    """)

    data = cursor.fetchall()

    categories = []
    amounts = []

    for row in data:
        categories.append(row[0])
        amounts.append(row[1])

    plt.pie(amounts, labels=categories, autopct='%1.1f%%')

    plt.title("Expense Distribution")

    plt.show(block=True)

def delete_expense():

    expense_id = input("Enter Expense ID to Delete: ")

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (expense_id,)
    )

    conn.commit()

    print("Expense Deleted Successfully!")

while True:

    print("\n-------EXPENSE TRACKER-------")

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Show Chart")
    print("5. Delete Expense")
    print("6. Exit")

    choice = input("Enter Your Choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        view_expenses()

    elif choice == "3":
        total_expense()

    elif choice == "4":
        show_chart()

    elif choice == "5":
        delete_expense()

    elif choice == "6":
        print("Thank you for using expense tracker")
        break

    else:
        print("Invalid Choice")  
        
