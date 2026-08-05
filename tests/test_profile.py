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


def test_profile_unauthenticated(client):
    response = client.get("/profile", follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to view your profile." in response.data
    assert b"Sign in" in response.data


def test_profile_authenticated(client):
    client.post(
        "/login",
        data={"email": "demo@spendly.com", "password": "demo123"},
        follow_redirects=True
    )
    
    response = client.get("/profile")
    assert response.status_code == 200
    assert b"Welcome back!" in response.data
    assert b"Demo User" in response.data
    assert b"demo@spendly.com" in response.data

