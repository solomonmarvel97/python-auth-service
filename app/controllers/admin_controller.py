from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.admin_model import User
from ..helpers.auth import decode_access_token, hash_password, verify_token
from ..schemas.admin_schema import UserCreate, UserVerify
import random
from ..helpers.access_code import AccessCode
from ..helpers.access_code import generate_code, save_access_code
from ..helpers.auth import hash_password, create_access_token, verify_password
from ..schemas.admin_schema import UserLogin, Token, UserExistQuery


def create_user(db: Session, user_data: UserCreate):
    """
    Creates a new user in the database.

    Args:
        db (Session): The database session.
        user_data (UserCreate): The data for the new user.

    Returns:
        User: The created user object, or None if the email is already registered.

    This function checks if a user with the given email already exists. If not,
    it hashes the provided password, creates a new User record, and saves it in the database.
    It also generates and saves an access code for the new user.
    """
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        return None  # Email already exists

    hashed_password = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_code = generate_code()
    save_access_code(db, new_user.id, access_code)

    return new_user


def verify_user_account(db: Session, user_verify: UserVerify) -> bool:
    """
    Verifies a user's account using an access code.

    Args:
        db (Session): The database session.
        user_verify (UserVerify): The schema containing the user ID and access code.

    Returns:
        bool: True if the account is successfully verified, False otherwise.

    This function checks if the provided access code matches the one stored for the user.
    If it matches, the user's account is marked as verified, and the function returns True.
    The access code record is then deleted. If the code does not match, the function returns False.
    """
    user_id = user_verify.user_id
    code = user_verify.code

    access_code_record = (
        db.query(AccessCode)
        .filter(AccessCode.user_id == user_id, AccessCode.code == code)
        .first()
    )
    if access_code_record:
        # Update the user's verification status
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.account_status = True
            db.add(user)

        # Delete the access code record
        db.delete(access_code_record)
        db.commit()
        return True
    else:
        return False


def login_user(db: Session, user_login: UserLogin) -> Token:
    """
    Authenticates a user and generates a JWT token.

    Args:
        db (Session): The database session.
        user_login (UserLogin): The login credentials of the user.

    Returns:
        Token: The JWT token for the authenticated user.

    Raises:
        HTTPException: An exception with status code 401 if authentication fails.
    """
    user = db.query(User).filter(User.email == user_login.email).first()
    if user and verify_password(user_login.password, user.hashed_password):
        access_token = create_access_token(data={"sub": user.id})
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(status_code=401, detail="Incorrect username or password")


def check_user_exists(db: Session, query: UserExistQuery) -> bool:
    """
    Checks if a user exists in the database.

    Args:
        db (Session): The database session.
        query (UserExistQuery): Query parameters containing user ID and/or email.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    if query.user_id:
        return db.query(User).filter(User.id == query.user_id).first() is not None
    elif query.email:
        return db.query(User).filter(User.email == query.email).first() is not None
    return False


def refresh_access_token(token: str) -> dict:
    """
    Refreshes an access token using a refresh token.

    Args:
        refresh_token (str): The refresh token provided by the user.

    Returns:
        dict: Contains the new access token if the refresh token is valid.

    Raises:
        HTTPException: If the refresh token is invalid or expired.
    """
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user_id = decode_access_token(token)
    print(user_id)
    new_access_token = create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token, "token_type": "bearer"}
