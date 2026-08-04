import sqlite3
import os
from werkzeug.security import generate_password_hash

# Path to SQLite database file in the project root directory
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "spendly.db")


def get_db():
    """
    Returns a SQLite database connection with row_factory set to sqlite3.Row
    and foreign key enforcement enabled.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """
    Creates the database tables (users and expenses) if they do not already exist.
    """
    conn = get_db()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)
    conn.close()


def seed_db():
    """
    Seeds the database with initial demo user and 8 sample expenses across all categories.
    Prevents duplicate insertion if data already exists.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if users already exist to avoid duplicate seeding
    cursor.execute("SELECT COUNT(*) FROM users;")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return

    # Insert Demo User
    password_hash = generate_password_hash("demo123")
    cursor.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?);",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    # Sample expenses covering all 7 categories: Food, Transport, Bills, Health, Entertainment, Shopping, Other
    sample_expenses = [
        (user_id, 45.50, "Food", "2026-08-01", "Grocery shopping at Supermarket"),
        (user_id, 12.00, "Transport", "2026-08-02", "Subway monthly fare top-up"),
        (user_id, 85.00, "Bills", "2026-08-03", "Electricity bill"),
        (user_id, 150.00, "Health", "2026-08-03", "Annual health checkup"),
        (user_id, 25.00, "Entertainment", "2026-08-04", "Cinema movie ticket"),
        (user_id, 65.00, "Shopping", "2026-08-04", "New running shoes"),
        (user_id, 15.00, "Other", "2026-08-04", "Stationery items"),
        (user_id, 32.80, "Food", "2026-08-04", "Dinner with colleagues"),
    ]

    cursor.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?);",
        sample_expenses,
    )
    conn.commit()
    conn.close()
