"""Command-line Expense Tracker. Run:  python main.py"""
import sys

import database
import services
from logger import get_logger

log = get_logger(__name__)


def ask(prompt, validator):
    """Keep asking until the validator accepts the input."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as err:
            print(f"  ⚠ {err}")


def add_expense() -> None:
    amount = ask("Amount: ", services.validate_amount)
    category = ask("Category (Food, Travel...): ", services.validate_category)
    description = input("Description (optional): ").strip()
    when = ask("Date YYYY-MM-DD (Enter = today): ", services.validate_date)
    expense_id = database.add_expense(amount, category, description, when)
    print(f"✅ Expense #{expense_id} added.")


def view_expenses() -> None:
    expenses = database.get_all_expenses()
    if not expenses:
        print("No expenses yet.")
        return
    print(f"\n{'ID':<5}{'Date':<12}{'Category':<14}{'Amount':>12}  Description")
    for e in expenses:
        print(f"{e['id']:<5}{e['date']:<12}{e['category']:<14}{e['amount']:>12,.2f}  {e['description'] or ''}")
    total = sum(e["amount"] for e in expenses)
    print(f"\nTotal: {services.format_money(total)}")


def delete_expense() -> None:
    raw = input("Expense ID to delete: ").strip()
    try:
        expense_id = int(raw)
    except ValueError:
        print("  ⚠ ID must be a number.")
        return
    if database.delete_expense(expense_id):
        print("🗑 Deleted.")
    else:
        print("No expense with that ID.")


def category_report() -> None:
    rows = database.totals_by_category()
    if not rows:
        print("No expenses yet.")
        return
    print("\nSpending by category")
    for r in rows:
        print(f"  {r['category']:<14}{services.format_money(r['total']):>14}")


def monthly_report() -> None:
    rows = database.totals_by_month()
    if not rows:
        print("No expenses yet.")
        return
    print("\nSpending by month")
    for r in rows:
        print(f"  {r['month']:<10}{services.format_money(r['total']):>14}")


MENU = {
    "1": ("Add expense", add_expense),
    "2": ("View expenses", view_expenses),
    "3": ("Delete expense", delete_expense),
    "4": ("Category report", category_report),
    "5": ("Monthly report", monthly_report),
}


def main() -> None:
    try:
        database.create_table()
    except database.DatabaseError as err:
        print(f"Startup error: {err}")
        return

    print("=== Expense Tracker ===")
    while True:
        print()
        for key, (label, _) in MENU.items():
            print(f"{key}. {label}")
        print("6. Exit")
        try:
            choice = input("Choose: ").strip()
            if choice == "6":
                print("Bye! 👋")
                break
            if choice in MENU:
                MENU[choice][1]()
            else:
                print("Invalid choice, enter a number from 1 to 6.")
        except database.DatabaseError as err:
            print(f"Database problem: {err}")
        except (KeyboardInterrupt, EOFError):
            print("\nBye! 👋")
            break
        except Exception:
            log.exception("Unexpected error")
            print("Something went wrong. Details are in expense_tracker.log")


if __name__ == "__main__":
    sys.exit(main())
