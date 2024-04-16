# auth.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from dotenv import load_dotenv
import os

load_dotenv()

# Configuration for JWT (JSON Web Token)
# Secret key for JWT encoding/decoding. Replace with a secure key.
SECRET_KEY = os.getenv("SECRET")
ALGORITHM = "HS256"  # Algorithm used for JWT encoding/decoding.
# The expiration time in minutes for the access token.
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

# Configuration for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): The data to be included in the token. Usually contains user identification info.

    Returns:
        str: A JWT encoded as a string.

    This function creates a JWT token by encoding the provided data along with an expiry time.
    The token can be used for authentication and authorization purposes.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> str:
    """
    Extract data from token

    Args:
        token (str): The parsed in token from the request body

    Returns:
        str: The user id extracted from the existing token

    This function creates a JWT token by encoding the provided data along with an expiry time.
    The token can be used for authentication and authorization purposes.
    """
    # Extract user ID from refresh token and generate a new access token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    return user_id


def verify_token(token: str) -> bool:
    """
    Verifies a JWT token.

    Args:
        token (str): The JWT token to be verified.

    Returns:
        bool: True if the token is valid, False otherwise.

    This function decodes the JWT token using the secret key and checks its validity.
    It returns True if the token is valid and the payload (such as user_id) can be retrieved.
    If the token is invalid or expired, it returns False.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        return user_id is not None
    except JWTError:
        return False


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain text password to be hashed.

    Returns:
        str: The hashed password.

    This function takes a plain text password and hashes it using bcrypt algorithm.
    The hashed password can then be safely stored in the database.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.

    This function uses bcrypt to compare a plain text password with a hashed password.
    It is used primarily for user authentication during login.
    """
    return pwd_context.verify(plain_password, hashed_password)
