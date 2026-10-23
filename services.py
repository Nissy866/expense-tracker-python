"""Input validation shared by the CLI and the web app."""
from datetime import date, datetime


def validate_amount(raw) -> float:
    try:
        amount = float(str(raw).strip())
    except ValueError:
        raise ValueError("Amount must be a number, for example 250 or 99.50")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0")
    return round(amount, 2)


def validate_category(raw) -> str:
    category = str(raw).strip().title()
    if not category:
        raise ValueError("Category cannot be empty")
    return category


def validate_date(raw) -> str:
    """Accepts YYYY-MM-DD. Empty input means today."""
    raw = str(raw).strip()
    if not raw:
        return str(date.today())
    try:
        return datetime.strptime(raw, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must look like 2026-10-23")


def format_money(value: float) -> str:
    return f"₹{value:,.2f}"
