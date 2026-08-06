import pytest
from app import app
from database import db


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Fixture that configures Flask app for testing with a temp database."""
    db_file = tmp_path / "test_spendly.db"
    monkeypatch.setattr(db, "DB_PATH", str(db_file))

    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.init_db()
        db.seed_db()

    with app.test_client() as client:
        yield client


def login_demo_user(client):
    """Helper to log in the default demo user."""
    return client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
        follow_redirects=True,
    )


# ============================================================================
# Authentication Checks
# ============================================================================

def test_profile_unauthenticated(client):
    """Unauthenticated GET /profile redirects to login."""
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to view your profile." in response.data
    assert b"Sign in" in response.data


def test_profile_unauthenticated_with_query_params(client):
    """Unauthenticated GET /profile with filter/preset parameters redirects to login."""
    response_preset = client.get("/profile?preset=this_month", follow_redirects=True)
    assert response_preset.status_code == 200
    assert b"Please log in to view your profile." in response_preset.data

    response_dates = client.get(
        "/profile?start_date=2026-08-01&end_date=2026-08-05",
        follow_redirects=True,
    )
    assert response_dates.status_code == 200
    assert b"Please log in to view your profile." in response_dates.data


# ============================================================================
# Profile Page Structure & UI Elements
# ============================================================================

def test_profile_authenticated_layout_and_form(client):
    """Authenticated user sees identity info, stats, date filter form, and quick presets."""
    login_demo_user(client)

    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Welcome back!" in response.data
    assert b"Demo User" in response.data
    assert b"demo@spendly.com" in response.data

    # Check presence of date filter form
    assert b'name="start_date"' in response.data
    assert b'name="end_date"' in response.data
    assert b"Filter" in response.data

    # Check presence of preset buttons
    assert b"All Time" in response.data
    assert b"This Month" in response.data
    assert b"Last 3 Months" in response.data
    assert b"Last 6 Months" in response.data


# ============================================================================
# Date Range Filter Tests (Happy Path & Open-Ended)
# ============================================================================

def test_profile_date_filter_valid_range(client):
    """Valid start_date and end_date filter metrics, recent transactions, and retain inputs."""
    login_demo_user(client)

    # Date range 2026-08-01 to 2026-08-02:
    # 2026-08-01: Grocery shopping (45.50)
    # 2026-08-02: Subway monthly fare top-up (12.00)
    # Total spent: 57.50, 2 transactions
    response = client.get("/profile?start_date=2026-08-01&end_date=2026-08-02")
    assert response.status_code == 200

    assert b"57.50" in response.data
    assert b"Grocery shopping at Supermarket" in response.data
    assert b"Subway monthly fare top-up" in response.data

    # Excluded expenses outside range
    assert b"Electricity bill" not in response.data
    assert b"Annual health checkup" not in response.data

    # Input state persistence
    assert b'value="2026-08-01"' in response.data
    assert b'value="2026-08-02"' in response.data
    assert b"Clear Filter" in response.data


def test_profile_date_filter_open_ended_start_date(client):
    """Providing only start_date filters expenses on or after start date."""
    login_demo_user(client)

    # Range: 2026-08-03 onwards
    # Expenses on 2026-08-03 and 2026-08-04:
    # 85.00 + 150.00 + 25.00 + 65.00 + 15.00 + 32.80 = 372.80 (6 transactions)
    response = client.get("/profile?start_date=2026-08-03")
    assert response.status_code == 200

    assert b"372.80" in response.data
    assert b"Cinema movie ticket" in response.data
    assert b"Annual health checkup" in response.data

    # Excluded expenses before 2026-08-03
    assert b"Grocery shopping at Supermarket" not in response.data
    assert b"Subway monthly fare top-up" not in response.data

    # Retains input value
    assert b'value="2026-08-03"' in response.data


def test_profile_date_filter_open_ended_end_date(client):
    """Providing only end_date filters expenses on or before end date."""
    login_demo_user(client)

    # Range: up to 2026-08-02
    # Expenses on 2026-08-01 & 2026-08-02: Total 57.50 (2 transactions)
    response = client.get("/profile?end_date=2026-08-02")
    assert response.status_code == 200

    assert b"57.50" in response.data
    assert b"Grocery shopping at Supermarket" in response.data
    assert b"Subway monthly fare top-up" in response.data

    # Excluded expenses after 2026-08-02
    assert b"Electricity bill" not in response.data
    assert b"Cinema movie ticket" not in response.data

    # Retains input value
    assert b'value="2026-08-02"' in response.data


# ============================================================================
# Quick Presets Tests
# ============================================================================

def test_profile_date_filter_preset_this_month(client):
    """preset=this_month highlights button and filters data for current month."""
    login_demo_user(client)

    response = client.get("/profile?preset=this_month")
    assert response.status_code == 200
    assert b"This Month" in response.data
    assert b"active" in response.data


def test_profile_date_filter_preset_last_3_months(client):
    """preset=last_3_months highlights button."""
    login_demo_user(client)

    response = client.get("/profile?preset=last_3_months")
    assert response.status_code == 200
    assert b"Last 3 Months" in response.data
    assert b"active" in response.data


def test_profile_date_filter_preset_last_6_months(client):
    """preset=last_6_months highlights button."""
    login_demo_user(client)

    response = client.get("/profile?preset=last_6_months")
    assert response.status_code == 200
    assert b"Last 6 Months" in response.data
    assert b"active" in response.data


def test_profile_date_filter_preset_all_time(client):
    """preset=all_time resets filters and displays all-time data."""
    login_demo_user(client)

    # All-time total across all 8 seeded expenses: 430.30
    response = client.get("/profile?preset=all_time")
    assert response.status_code == 200
    assert b"430.30" in response.data
    assert b"All Time" in response.data
    assert b"active" in response.data


# ============================================================================
# Validation Error Handling
# ============================================================================

def test_profile_date_filter_invalid_range(client):
    """start_date after end_date flashes error message and falls back to all-time data."""
    login_demo_user(client)

    response = client.get("/profile?start_date=2026-08-10&end_date=2026-08-01")
    assert response.status_code == 200
    assert b"Start date cannot be after end date." in response.data
    # Fallback to all-time data
    assert b"430.30" in response.data


# ============================================================================
# Category Breakdown Filter Test
# ============================================================================

def test_profile_category_breakdown_filtered(client):
    """Category breakdown totals calculate based only on filtered expenses."""
    login_demo_user(client)

    # Filter strictly for 2026-08-01 (Only Food category: 45.50)
    response = client.get("/profile?start_date=2026-08-01&end_date=2026-08-01")
    assert response.status_code == 200

    assert b"45.50" in response.data
    assert b"Food" in response.data
    # Bills (85.00 on Aug 3) should not be calculated in this category breakdown
    assert b"85.00" not in response.data


# ============================================================================
# Regression Checks
# ============================================================================

def test_profile_regression_user_info_intact(client):
    """Applying date filters does not compromise user identity or profile details."""
    login_demo_user(client)

    response = client.get("/profile?start_date=2026-08-01&end_date=2026-08-02")
    assert response.status_code == 200
    assert b"Demo User" in response.data
    assert b"demo@spendly.com" in response.data
    assert b"Member since" in response.data


def test_profile_date_filter_malformed_input(client):
    """Malformed date strings trigger validation error message."""
    login_demo_user(client)

    response = client.get("/profile?start_date=invalid-date&end_date=not-a-date")
    assert response.status_code == 200
    assert b"Invalid date format provided." in response.data

