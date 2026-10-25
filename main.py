import json
from datetime import datetime
DATA_FILE = "expenses.json"
income = 0.0
expenses = 0.0
transactions = []

def show_menu():
    print("\n===== EXPENSE TREACKER PRO =====")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Category-wise Report")
    print("6. Monthly Report")
    print("7. Exit")

def get_amount():
    while True :
        try:
            amount = float(input("Enter amount :"))
            if amount <= 0 :
                print("Amount must be greater than zero!")
                continue
            return amount
        except ValueError:
            print("Invalid amount!Enter a number")

def add_transaction(transaction_type,amount):
    transactions.append({
        "type": transaction_type,
        "amount": amount,
        "date": datetime.now().strftime("%d-%m-%y%H:%M")})

def save_data():
    data = {
        "income": income,
        "expenses": expenses,
        "transactions": transactions
    }
    with open(DATA_FILE,"w",encoding="utf-8") as file :
        json.dump(data,file,indent=4)
    print("Data saved successfully")

def load_data():
    global income,expenses,transactions
    try:
        with open(DATA_FILE,"r",encoding="utf-8") as file :
            data = json.load(file)
            income = data.get("income",0.0)
            expenses = data.get("expenses",0.0)
            transactions = data.get("transactions",[])
            print("Previous data loaded successfully")
    except FileNotFoundError :
        print("First run : Starting with fresh data.")

def view_transactions():
    print("\n=====TRANSACTION HISTORY=====")
    if not transactions:
        print("NO transactions yet!")
        return
    for item in transactions:
        print(
            f"{item['date']} |"
            f"{item['type']} |"
            f"{item.get('category','-')} |"
            f"Rs.{item['amount']:.2f}"
        )

def category_report ():
    print("\n=====CATEGORY-WISE REPORT=====")
    category_totals = {}
    for item in transactions:
        print("DEBUG:",item)
        if item.get("type","").strip().lower()=="expense":
            category = item.get("category","Other")
            amount = float(item.get("amount",0))
    category_totals[category]=(category_totals.get(category, 0)+amount)
    if not category_totals:
            print("No expense recorded yet!")
            return
    for category,total in category_totals.items():
            print(f"{category}:Rs.{total:.2f}")

def monthly_report():
    print("\n===== MONTHLY REPORT =====")

    current_month = datetime.now().strftime("%m-%y")
    monthly_income = 0.0
    monthly_expenses = 0.0

    for item in transactions:
        transaction_date = None

        for date_format in (
            "%d-%m-%y %H:%M",
            "%d-%m-%y%H:%M",
            "%d-%m-%Y %H:%M",
            "%d-%m-%Y%H:%M"
        ):
            try:
                transaction_date = datetime.strptime(
                    item["date"], date_format
                )
                break
            except (ValueError, KeyError):
                continue

        if transaction_date is None:
            continue

        if transaction_date.strftime("%m-%y") == current_month:
            amount = float(item.get("amount", 0))

            if item.get("type") == "Income":
                monthly_income += amount
            elif item.get("type") in ("Expense", "Expenses"):
                monthly_expenses += amount

    print(f"Month: {datetime.now().strftime('%B %Y')}")
    print(f"Total Income: Rs. {monthly_income:.2f}")
    print(f"Total Expenses: Rs. {monthly_expenses:.2f}")
    print(
        f"Remaining Balance: Rs. "
        f"{monthly_income - monthly_expenses:.2f}"
    )

load_data()

while True :
    show_menu()
    choice = input("Enter your choice : ")
    if choice == "1" :
        amount = get_amount()
        income += amount
        add_transaction("Income",amount)
        save_data()
        print(f"Income add successfully : ${amount:.2f}")
    elif choice == "2" :
        amount = get_amount()
        print("choose category :")
        print("1. Food")
        print("2. Travel")
        print("3. Shopping")
        print("4. Bills")
        print("5. Other")
        category_choice = input("Enter category number :")
        categories = {
            "1": "Food",
            "2": "Travel",
            "3": "Shopping",
            "4": "Bills",
            "5": "Other"
        }
        if category_choice not in categories:
            print("Invalid category!")
            continue
        category = categories[category_choice]
        expenses += amount
        add_transaction("Expense",amount)
        transactions[-1]["category"] = category
        save_data()
        print(f"Expense added : Rs. {amount:.2f}")
        print(f"Category : {category}")
    elif choice == "3" :
        view_transactions()
    elif choice == "4" :
        balance = income - expenses
        print(f"Total Income : Rs. {income:.2f}")
        print(f"Total Expense : Rs. {expenses:.2f}")
        print(f"Current balance : Rs. {balance:.2f}")
    elif choice == "5" :
        category_report  ()
    elif choice == "6":
        monthly_report()
    elif choice == "7":
        print("Thank you for using Expense Tracker Pro")
        break
    else :
        print("Invalid choice ! Please try 1 to 6.")
