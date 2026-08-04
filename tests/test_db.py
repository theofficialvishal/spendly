import sqlite3
import os
import pytest
from database import db


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Fixture that redirects database/db.py DB_PATH to a temporary file."""
    db_file = tmp_path / "test_spendly.db"
    monkeypatch.setattr(db, "DB_PATH", str(db_file))
    return db_file


def test_init_db_creates_tables(test_db):
    db.init_db()
    conn = db.get_db()
    cursor = conn.cursor()
    
    # Check users table structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    assert cursor.fetchone() is not None

    # Check expenses table structure
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='expenses';")
    assert cursor.fetchone() is not None
    conn.close()


def test_seed_db_populates_data_and_prevents_duplicates(test_db):
    db.init_db()
    db.seed_db()

    conn = db.get_db()
    cursor = conn.cursor()

    # Check demo user
    cursor.execute("SELECT * FROM users WHERE email = ?", ("demo@spendly.com",))
    user = cursor.fetchone()
    assert user is not None
    assert user["name"] == "Demo User"

    # Check 8 sample expenses
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user["id"],))
    expenses = cursor.fetchall()
    assert len(expenses) == 8

    # Verify all 7 categories are present
    categories = {e["category"] for e in expenses}
    expected_categories = {"Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"}
    assert categories == expected_categories

    conn.close()

    # Run seed_db again to test idempotency
    db.seed_db()
    conn2 = db.get_db()
    cursor2 = conn2.cursor()
    cursor2.execute("SELECT COUNT(*) FROM users;")
    assert cursor2.fetchone()[0] == 1

    cursor2.execute("SELECT COUNT(*) FROM expenses;")
    assert cursor2.fetchone()[0] == 8
    conn2.close()


def test_foreign_key_constraint(test_db):
    db.init_db()
    conn = db.get_db()
    
    # Attempt inserting an expense with invalid user_id should raise IntegrityError
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?);",
            (999, 50.00, "Food", "2026-08-01")
        )
    conn.close()


def test_unique_email_constraint(test_db):
    db.init_db()
    db.seed_db()
    conn = db.get_db()

    # Attempt inserting user with duplicate email should raise IntegrityError
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?);",
            ("Another User", "demo@spendly.com", "hash123")
        )
    conn.close()
