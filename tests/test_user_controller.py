from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app

from app.config.database import Base
from sqlalchemy.orm import sessionmaker
from app.config.database import get_db as original_get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[original_get_db] = override_get_db

def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)


def test_create_user():
    """
    Test the user creation endpoint.

    This test case verifies that a new user can be successfully created via the `/signup` endpoint.
    It asserts that the response status is 200 OK and the response data matches the input data.
    """

    # Setup database and test data
    user_data = {"email": "test@example.com", "username": "testuser", "password": "testpassword"}
    response = client.post("/signup", json=user_data)
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_login_user():
    """
    Test the user login endpoint.

    This test case ensures that a user can log in with valid credentials.
    It checks that the response status is 200 OK and an access token is received.
    """
    # Assuming user is already created
    user_login = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/login", json=user_login)
    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_verify_user_account():
    """
    Test the user account verification endpoint.

    This test creates a new user and then tests the verification process using a simulated access code.
    It checks that the response status is 200 OK and the account is marked as verified.
    """
    # First, create a user
    user_data = {"email": "verify@example.com", "username": "verifyuser", "password": "verifypassword"}
    response = client.post("/signup", json=user_data)
    assert response.status_code == 200

    # Extract user ID and access code from the response
    user_id = response.json()["id"]
    # Here, assume the access code is stored or returned during signup for testing
    access_code = "123456"  # Replace with the actual code

    # Test the verification endpoint
    verify_data = {"user_id": user_id, "code": access_code}
    response = client.post("/verify-account", json=verify_data)
    assert response.status_code == 200
    assert response.json() == {"valid_account": True}

def test_check_user_exists():
    """
    Test the check if a user exists endpoint.

    This test creates a new user and then checks whether the user exists using the provided email.
    It tests both scenarios - where the user exists and where the user does not exist.
    """
    # Create a user
    user_data = {"email": "exists@example.com", "username": "existsuser", "password": "existspassword"}
    response = client.post("/signup", json=user_data)
    assert response.status_code == 200

    # Check if the user exists using email
    query_params = {"email": "exists@example.com"}
    response = client.get("/check-user-exists", params=query_params)
    assert response.status_code == 200
    assert response.json() == {"valid_account": True}

    # Check if a non-existing user exists
    query_params = {"email": "nonexistent@example.com"}
    response = client.get("/check-user-exists", params=query_params)
    assert response.status_code == 200
    assert response.json() == {"valid_account": False}

def test_refresh_access_token():
    """
    Test the access token refresh functionality.

    This test logs in a user to obtain a refresh token and then attempts to refresh the access token using this token.
    It asserts that a new access token is successfully obtained upon token refresh.
    """
    # Create a user and log in to get a token
    user_data = {"email": "refresh@example.com", "username": "refreshuser", "password": "refreshpassword"}
    client.post("/signup", json=user_data)
    login_data = {"email": "refresh@example.com", "password": "refreshpassword"}
    login_response = client.post("/login", json=login_data)
    refresh_token = login_response.json()["access_token"]

    # Test the refresh token endpoint
    response = client.post("/refresh-token", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"