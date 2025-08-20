import argparse
import json
import os
import csv
from datetime import datetime


DATA_FILE = "expenses.json"
BUDGET_FILE = "budgets.json"


def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=2)


def add_expense(amount, description, category, date=None):
    expenses = load_expenses()
    expense_id = (max([e["id"] for e in expenses], default=0) + 1)  # Auto-increment ID

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Input validation: amount positive, no empty description
    if amount <= 0:
        print("Error: Amount must be positive.")
        return
    if not description:
        print("Error: Description is required.")
        return

    expense = {
        "id": expense_id,
        "amount": amount,
        "description": description,
        "category": category,
        "date": date
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Added expense #{expense_id}: {description} - ${amount:.2f} [{category}] on {date}")


def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
        return
    for expense in expenses:
        print(
            f"ID: {expense['id']} | ${expense['amount']:.2f} | {expense['description']} | {expense['category']} | {expense['date']}"
        )


def update_expense(expense_id, amount=None, description=None, category=None, date=None):
    expenses = load_expenses()
    for expense in expenses:
        if expense['id'] == expense_id:
            if amount is not None:
                if amount <= 0:
                    print("Error: Amount must be positive.")
                    return
                expense['amount'] = amount
            if description is not None:
                expense['description'] = description
            if category is not None:
                expense['category'] = category
            if date is not None:
                expense['date'] = date
            save_expenses(expenses)
            print(f"Expense ID {expense_id} updated.")
            return
    print(f"Expense ID {expense_id} not found.")


def delete_expense(expense_id):
    expenses = load_expenses()
    new_expenses = [e for e in expenses if e['id'] != expense_id]
    if len(new_expenses) == len(expenses):
        print(f"Expense ID {expense_id} not found.")
        return
    save_expenses(new_expenses)
    print(f"Expense ID {expense_id} deleted.")


def summary_all_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize.")
        return

    total = sum(e['amount'] for e in expenses)
    count = len(expenses)
    average = total / count if count else 0

    print(f"Summary of all expenses:")
    print(f"  Total spent: ${total:.2f}")
    print(f"  Number of expenses: {count}")
    print(f"  Average expense amount: ${average:.2f}")


def summary_month(month, year=None):
    expenses = load_expenses()
    if not expenses:
        print("No expenses to summarize for this month.")
        return
    if year is None:
        year = datetime.now().year

    # Filter for matching year and month
    filtered = [
        e for e in expenses
        if e['date'].startswith(f"{year}-{int(month):02d}")
    ]
    total = sum(e['amount'] for e in filtered)
    count = len(filtered)
    print(f"Summary for {year}-{int(month):02d}:")
    print(f"  Total spent: ${total:.2f}")
    print(f"  Number of expenses: {count}")
    if count == 0:
        print("  No expenses recorded for this month.")


def summary_category(category):
    expenses = load_expenses()
    filtered = [e for e in expenses if e['category'].lower() == category.lower()]
    total = sum(e['amount'] for e in filtered)
    count = len(filtered)
    print(f"Summary for category '{category}':")
    print(f"  Total spent: ${total:.2f}")
    print(f"  Number of expenses: {count}")
    if count == 0:
        print("  No expenses recorded for this category.")


def filter_expenses_by_category(category):
    expenses = load_expenses()
    filtered = [e for e in expenses if e['category'].lower() == category.lower()]
    if not filtered:
        print(f"No expenses found in category '{category}'.")
        return
    for expense in filtered:
        print(
            f"ID: {expense['id']} | ${expense['amount']:.2f} | {expense['description']} | {expense['category']} | {expense['date']}"
        )


def load_budgets():
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, "r") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

def save_budgets(budgets):
    with open(BUDGET_FILE, "w") as f:
        json.dump(budgets, f, indent=2)


def set_budget(month, year, amount):
    budgets = load_budgets()
    key = f"{year}-{int(month):02d}"
    budgets[key] = amount
    save_budgets(budgets)
    print(f"Budget for {key} set to ${amount:.2f}")


def budget_status(month, year=None):
    if year is None:
        year = datetime.now().year
    budgets = load_budgets()
    key = f"{year}-{int(month):02d}"
    monthly_budget = budgets.get(key)
    expenses = load_expenses()
    monthly_expenses = [e for e in expenses if e['date'].startswith(key)]
    total_spent = sum(e['amount'] for e in monthly_expenses)

    print(f"Budget status for {key}:")
    print(f"  Total spent: ${total_spent:.2f}")
    if monthly_budget is not None:
        print(f"  Budget: ${monthly_budget:.2f}")
        if total_spent > monthly_budget:
            print("  WARNING: Budget exceeded!")
        else:
            print(f"  You have ${monthly_budget - total_spent:.2f} left.")
    else:
        print("  No budget set for this month.")


def export_expenses_to_csv(filename="expenses_export.csv"):
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return

    # Determine the fieldnames based on your data model
    fieldnames = ["id", "amount", "description", "category", "date"]

    try:
        with open(filename, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for expense in expenses:
                writer.writerow(expense)
        print(f"Expenses exported to {filename}")
    except Exception as e:
        print(f"Error exporting expenses: {e}")


def main():
    parser = argparse.ArgumentParser(description="Expense Tracker CLI")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Add expense command
    add_parser = subparsers.add_parser("add", help="Add a new expense")
    add_parser.add_argument("--amount", type=float, required=True, help="Expense amount")
    add_parser.add_argument("--description", type=str, required=True, help="Expense description")
    add_parser.add_argument("--category", type=str, default="Other", help="Expense category")
    add_parser.add_argument("--date", type=str, help="Date for the expense (YYYY-MM-DD)")

    # List expenses command
    subparsers.add_parser("list", help="List all expenses")

    # Update expense command
    update_parser = subparsers.add_parser("update", help="Update an expense")
    update_parser.add_argument("id", type=int, help="ID of the expense to update")
    update_parser.add_argument("--amount", type=float, help="New amount")
    update_parser.add_argument("--description", type=str, help="New description")
    update_parser.add_argument("--category", type=str, help="New category")
    update_parser.add_argument("--date", type=str, help="New date (YYYY-MM-DD)")

    # Delete expense command
    delete_parser = subparsers.add_parser("delete", help="Delete an expense")
    delete_parser.add_argument("id", type=int, help="ID of the expense to delete")

    # Summarize all expenses
    subparsers.add_parser("summary", help="Summary of all expenses.")

    # Summarize by month
    summary_month_parser = subparsers.add_parser("summary-month", help="Show summary for a specific month of current year")
    summary_month_parser.add_argument("month", type=int, help="Month number (1-12)")

    # Summarize by category
    summary_cat_parser = subparsers.add_parser("summary-category", help="Show summary for a specific category.")
    summary_cat_parser.add_argument("category", type=str, help="Category to summarize")

    # Filter by category
    filter_parser = subparsers.add_parser("filter-category", help="List expenses by category")
    filter_parser.add_argument("category", type=str, help="Category to filter by")

    set_budget_parser = subparsers.add_parser("set-budget", help="Set budget for a specific month")
    set_budget_parser.add_argument("month", type=int, help="Month number (1-12)")
    set_budget_parser.add_argument("year", type=int, help="Year (e.g., 2025)")
    set_budget_parser.add_argument("amount", type=float, help="Budget amount")

    budget_status_parser = subparsers.add_parser("budget-status", help="Show budget status for a month")
    budget_status_parser.add_argument("month", type=int, help="Month number (1-12)")
    budget_status_parser.add_argument("--year", type=int, help="Year (default: current year)")

    export_parser = subparsers.add_parser("export-csv", help="Export all expenses to a CSV file")
    export_parser.add_argument("--filename", type=str, default="expenses_export.csv",
                               help="Export filename (default: expenses_export.csv)")

    args = parser.parse_args()

    if args.command == "add":
        add_expense(args.amount, args.description, args.category, args.date)
    elif args.command == "list":
        list_expenses()
    elif args.command == "update":
        update_expense(args.id, args.amount, args.description, args.category, args.date)
    elif args.command == "delete":
        delete_expense(args.id)
    elif args.command == "summary":
        summary_all_expenses()
    elif args.command == "summary-month":
        summary_month(args.month)
    elif args.command == "summary-category":
        summary_category(args.category)
    elif args.command == "filter-category":
        filter_expenses_by_category(args.category)
    elif args.command == "set-budget":
        set_budget(args.month, args.year, args.amount)
    elif args.command == "budget-status":
        budget_status(args.month, args.year)
    elif args.command == "export-csv":
        export_expenses_to_csv(args.filename)


if __name__ == "__main__":
    main()
