import pytest
from app import app
from database import db
from werkzeug.security import check_password_hash


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


def test_register_get_renders_template(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Create your account" in response.data


def test_register_success(client):
    response = client.post(
        "/register",
        data={
            "name": "New User",
            "email": "newuser@example.com",
            "password": "securepassword123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Registration successful. Please sign in." in response.data

    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?;", ("newuser@example.com",))
    user = cursor.fetchone()
    assert user is not None
    assert user["name"] == "New User"
    assert check_password_hash(user["password_hash"], "securepassword123")
    conn.close()


def test_register_duplicate_email(client):
    response = client.post(
        "/register",
        data={
            "name": "Duplicate User",
            "email": "demo@spendly.com",
            "password": "password123"
        },
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Email already registered. Please sign in." in response.data
