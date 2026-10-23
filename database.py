"""All SQLite database operations live here."""
import sqlite3
from contextlib import closing
from pathlib import Path

from logger import get_logger

log = get_logger(__name__)

DB_PATH = Path(__file__).parent / "expenses.db"


class DatabaseError(Exception):
    """Raised when a database operation fails."""


def _connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def create_table(db_path=DB_PATH) -> None:
    try:
        with closing(_connect(db_path)) as conn, conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    amount      REAL    NOT NULL CHECK (amount > 0),
                    category    TEXT    NOT NULL,
                    description TEXT,
                    date        TEXT    NOT NULL
                )
            """)
    except sqlite3.Error as err:
        log.error("create_table failed: %s", err)
        raise DatabaseError("Could not set up the database.")


def add_expense(amount, category, description, date, db_path=DB_PATH) -> int:
    try:
        with closing(_connect(db_path)) as conn, conn:
            cur = conn.execute(
                "INSERT INTO expenses (amount, category, description, date) VALUES (?, ?, ?, ?)",
                (amount, category, description, date),
            )
            log.info("Added expense id=%s amount=%s category=%s", cur.lastrowid, amount, category)
            return cur.lastrowid
    except sqlite3.Error as err:
        log.error("add_expense failed: %s", err)
        raise DatabaseError("Could not save the expense.")


def get_all_expenses(db_path=DB_PATH) -> list:
    try:
        with closing(_connect(db_path)) as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM expenses ORDER BY date DESC, id DESC")]
    except sqlite3.Error as err:
        log.error("get_all_expenses failed: %s", err)
        raise DatabaseError("Could not read expenses.")


def delete_expense(expense_id, db_path=DB_PATH) -> bool:
    try:
        with closing(_connect(db_path)) as conn, conn:
            cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            deleted = cur.rowcount > 0
            log.info("Delete id=%s -> %s", expense_id, "ok" if deleted else "not found")
            return deleted
    except sqlite3.Error as err:
        log.error("delete_expense failed: %s", err)
        raise DatabaseError("Could not delete the expense.")


def totals_by_category(db_path=DB_PATH) -> list:
    try:
        with closing(_connect(db_path)) as conn:
            rows = conn.execute(
                "SELECT category, SUM(amount) AS total FROM expenses GROUP BY category ORDER BY total DESC"
            )
            return [dict(r) for r in rows]
    except sqlite3.Error as err:
        log.error("totals_by_category failed: %s", err)
        raise DatabaseError("Could not build the category report.")


def totals_by_month(db_path=DB_PATH) -> list:
    try:
        with closing(_connect(db_path)) as conn:
            rows = conn.execute(
                "SELECT substr(date, 1, 7) AS month, SUM(amount) AS total "
                "FROM expenses GROUP BY month ORDER BY month DESC"
            )
            return [dict(r) for r in rows]
    except sqlite3.Error as err:
        log.error("totals_by_month failed: %s", err)
        raise DatabaseError("Could not build the monthly report.")
