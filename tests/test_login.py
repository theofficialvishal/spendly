import pytest
from flask import session
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


def test_login_get_renders_template(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Welcome back" in response.data
    assert b"Sign in to your Spendly account" in response.data


def test_login_success(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "demo123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome back, Demo User!" in response.data
    assert b"Sign out" in response.data

    with client.session_transaction() as sess:
        assert sess.get("user_id") is not None
        assert sess.get("user_name") == "Demo User"
        assert sess.get("user_email") == "demo@spendly.com"


def test_login_case_insensitive_email(client):
    response = client.post(
        "/login",
        data={
            "email": " DEMO@SPENDLY.COM ",
            "password": "demo123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Welcome back, Demo User!" in response.data


def test_login_invalid_password(client):
    response = client.post(
        "/login",
        data={
            "email": "demo@spendly.com",
            "password": "wrongpassword"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_nonexistent_email(client):
    response = client.post(
        "/login",
        data={
            "email": "nobody@spendly.com",
            "password": "demo123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Invalid email or password." in response.data


def test_login_missing_fields(client):
    response = client.post(
        "/login",
        data={
            "email": "",
            "password": ""
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Please provide both email and password." in response.data


def test_logout(client):
    # Log in first
    client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
        follow_redirects=True
    )

    # Perform logout
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out successfully." in response.data
    assert b"Sign in" in response.data

    with client.session_transaction() as sess:
        assert sess.get("user_id") is None


def test_already_logged_in_redirect_from_login(client):
    client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
        follow_redirects=True
    )

    response = client.get("/login", follow_redirects=True)
    assert response.status_code == 200
    assert b"You are already logged in." in response.data


def test_already_logged_in_redirect_from_register(client):
    client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
        follow_redirects=True
    )

    response = client.get("/register", follow_redirects=True)
    assert response.status_code == 200
    assert b"You are already logged in." in response.data
