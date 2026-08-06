from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db

app = Flask(__name__)
app.secret_key = "spendly-dev-secret-key"

# Initialize database schema and seed sample data
with app.app_context():
    init_db()
    seed_db()


def format_date_display(date_str):
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return dt.strftime("%d %b %Y")
    except (ValueError, TypeError):
        return date_str[:10]


def get_avatar_initials(name):
    if not name:
        return "U"
    parts = name.strip().split()
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def validate_iso_date(date_str):
    """Validates that a string is in YYYY-MM-DD format. Returns normalized string or empty string."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        return ""


def resolve_profile_date_filter(args):
    """
    Extracts and validates date filter parameters (preset, start_date, end_date).
    Returns (start_date, end_date, active_preset, flash_error_message).
    """
    preset = (args.get("preset") or "").strip().lower()
    start_date_str = (args.get("start_date") or "").strip()
    end_date_str = (args.get("end_date") or "").strip()

    start_date = ""
    end_date = ""
    error_msg = None

    if preset in ("all", "all_time"):
        start_date = ""
        end_date = ""
    elif preset == "this_month":
        today = date.today()
        start_date = today.replace(day=1).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif preset == "last_3_months":
        today = date.today()
        start_date = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    elif preset == "last_6_months":
        today = date.today()
        start_date = (today - timedelta(days=180)).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
    else:
        start_date = validate_iso_date(start_date_str)
        end_date = validate_iso_date(end_date_str)
        if (start_date_str and not start_date) or (end_date_str and not end_date):
            error_msg = "Invalid date format provided."

    if start_date and end_date and start_date > end_date:
        error_msg = "Start date cannot be after end date."
        start_date = ""
        end_date = ""
        preset = ""

    active_preset = preset if preset in ("this_month", "last_3_months", "last_6_months") else ""
    if not start_date and not end_date:
        active_preset = "all_time"

    return start_date, end_date, active_preset, error_msg


def build_date_where_clause(user_id, start_date, end_date):
    """Builds a SQL WHERE clause and parameters list for expense date filtering."""
    date_conditions = []
    query_params = [user_id]

    if start_date:
        date_conditions.append("date >= ?")
        query_params.append(start_date)
    if end_date:
        date_conditions.append("date <= ?")
        query_params.append(end_date)

    where_clause = "WHERE user_id = ?"
    if date_conditions:
        where_clause += " AND " + " AND ".join(date_conditions)

    return where_clause, tuple(query_params)


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if "user_id" in session:
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("profile"))

    if request.method == "POST":
        name = request.form.get("name")
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute("SELECT id FROM users WHERE email = ?;", (email,))
        if cursor.fetchone():
            conn.close()
            flash("Email already registered. Please sign in.", "error")
            return redirect(url_for("register"))

        # Insert new user
        password_hash = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?);",
            (name, email, password_hash)
        )
        conn.commit()
        conn.close()

        flash("Registration successful. Please sign in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("profile"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not email or not password:
            flash("Please provide both email and password.", "error")
            return redirect(url_for("login"))

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, password_hash FROM users WHERE email = ?;",
            (email,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("login"))

    user_id = session["user_id"]
    start_date, end_date, active_preset, error_msg = resolve_profile_date_filter(request.args)
    if error_msg:
        flash(error_msg, "error")

    where_clause, query_params = build_date_where_clause(user_id, start_date, end_date)

    conn = get_db()
    cursor = conn.cursor()
    try:
        # 1. Fetch User Identity
        cursor.execute("SELECT name, email, created_at FROM users WHERE id = ?;", (user_id,))
        user_row = cursor.fetchone()
        if not user_row:
            session.clear()
            flash("User not found. Please log in again.", "error")
            return redirect(url_for("login"))

        user_info = {
            "name": user_row["name"],
            "email": user_row["email"],
            "created_at": user_row["created_at"],
            "initials": get_avatar_initials(user_row["name"]),
            "joined_date": format_date_display(user_row["created_at"])
        }

        # 2. Fetch Aggregated Metrics (Total Spent, Total Transactions)
        cursor.execute(
            f"SELECT COALESCE(SUM(amount), 0) AS total_spent, COUNT(*) AS total_tx FROM expenses {where_clause};",
            query_params
        )
        metrics_row = cursor.fetchone()
        total_spent = float(metrics_row["total_spent"]) if metrics_row else 0.0
        total_transactions = metrics_row["total_tx"] if metrics_row else 0

        # 3. Fetch Recent Transactions
        cursor.execute(
            f"SELECT id, amount, category, date, description FROM expenses {where_clause} ORDER BY date DESC, id DESC LIMIT 5;",
            query_params
        )
        tx_rows = cursor.fetchall()
        recent_transactions = [
            {
                "id": row["id"],
                "amount": float(row["amount"]),
                "category": row["category"],
                "category_slug": row["category"].lower(),
                "date": format_date_display(row["date"]),
                "description": row["description"] or ""
            }
            for row in tx_rows
        ]

        # 4. Fetch Category Breakdown
        cursor.execute(
            f"SELECT category, SUM(amount) AS cat_sum FROM expenses {where_clause} GROUP BY category ORDER BY cat_sum DESC;",
            query_params
        )
        cat_rows = cursor.fetchall()
        category_breakdown = []
        max_cat_total = float(cat_rows[0]["cat_sum"]) if cat_rows else 1.0
        if max_cat_total <= 0:
            max_cat_total = 1.0

        for row in cat_rows:
            cat_sum = float(row["cat_sum"])
            pct = min(100, max(5, round((cat_sum / max_cat_total) * 100)))
            category_breakdown.append({
                "category": row["category"],
                "category_slug": row["category"].lower(),
                "amount": cat_sum,
                "percentage": pct
            })

        # Top category derived directly from breakdown (eliminates redundant query)
        top_category = category_breakdown[0]["category"] if category_breakdown else "N/A"

        stats = {
            "total_spent": total_spent,
            "total_transactions": total_transactions,
            "top_category": top_category
        }

    finally:
        conn.close()

    return render_template(
        "profile.html",
        user=user_info,
        stats=stats,
        recent_transactions=recent_transactions,
        category_breakdown=category_breakdown,
        start_date=start_date,
        end_date=end_date,
        active_preset=active_preset
    )


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
