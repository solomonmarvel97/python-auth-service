# app/routes/user_routes.py

from typing import Optional
from ..schemas.admin_schema import UserLogin, Token
from ..controllers.admin_controller import login_user
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query, HTTPException

from app.config.database import get_db
from ..schemas.admin_schema import (
    RefreshToken,
    UserCreate,
    UserOut,
    UserVerify,
    UserExistQuery,
)
from ..controllers.admin_controller import (
    create_user,
    refresh_access_token,
    verify_user_account,
    check_user_exists,
)

# Initialize the API router from FastAPI.
# This router will handle all endpoints related to user operations.
router = APIRouter()


@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint for user signup.

    This endpoint handles the creation of new users. It receives user data, processes it,
    and creates a new user record in the database.

    Args:
        user (UserCreate): The user data for the new user, received from the request body.
        db (Session): The database session dependency.

    Returns:
        UserOut: The created user's data, conforming to the UserOut schema.

    Raises:
        HTTPException: An exception with status code 400 if the email is already registered.
    """
    result = create_user(db, user)
    if result is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return result


@router.post("/verify-account")
def verify_account(user_verify: UserVerify, db: Session = Depends(get_db)):
    """
    Endpoint for verifying a user's account.

    This endpoint accepts a user ID and an access code and uses them to verify the user's account.

    Args:
        user_verify (UserVerify): The user ID and access code for verification.
        db (Session): Database session.

    Returns:
        dict: A message indicating success or failure of the verification.
    """
    if verify_user_account(db, user_verify):
        return {"message": "Account successfully verified."}
    else:
        raise HTTPException(
            status_code=400, detail="Invalid verification code or user ID"
        )


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint for user login.

    Args:
        user_login (UserLogin): The login credentials of the user.
        db (Session): Database session.

    Returns:
        Token: The JWT token for the authenticated user.
    """
    return login_user(db, user_login)


@router.get("/check-user-exists", response_model=dict)
async def check_user_exists_route(
    user_id: Optional[str] = Query(None, description="The user's unique identifier"),
    email: Optional[str] = Query(None, description="The user's email address"),
    db: Session = Depends(get_db)
):
    """
    Endpoint to check if a user exists based on user ID or email.

    Args:
        user_id (str, optional): The user ID to check. Defaults to None.
        email (str, optional): The email to check. Defaults to None.
        db (Session): Database session.

    Returns:
        dict: A dictionary containing a 'valid_account' key with a boolean value.
    """
    query = UserExistQuery(user_id=str(user_id))
    return {"valid_account": check_user_exists(db, query)}


@router.post("/refresh-token", response_model=dict)
def refresh_token(refresh_token: RefreshToken):
    """
    Endpoint for refreshing an access token.

    Args:
        refresh_token (str): The refresh token provided in the request body.

    Returns:
        dict: Contains the new access token.
    """
    token = refresh_token.refresh_token
    return refresh_access_token(token)
