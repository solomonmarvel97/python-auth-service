from pydantic import BaseModel, EmailStr


class CreateStaff(BaseModel):
    email: EmailStr


class UserOut(BaseModel):
    """
    Schema for user output.

    This schema defines the structure of the response body when user data is queried.
    It is typically used when returning user details in response to various API requests.

    Attributes:
        id (str): The unique identifier of the user, typically a UUID
        username (st): Generate random string username
        email (EmailStr): The email address of the user.
    """

    id: str
    email: EmailStr
    username: str
    account_status: str


class Token(BaseModel):
    """
    Schema for JWT access token.

    This schema defines the structure of a JWT access token, which is used for authentication
    and authorization within the application.

    Attributes:
        access_token (str): The actual JWT token.
        token_type (str): The type of token, typically 'bearer'.
    """

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """
    Schema for data encoded in the JWT token.

    This schema is used to represent the data that is contained within a JWT token,
    such as the user's identity.

    Attributes:
        user_id (str): The unique identifier of the user encoded in the token.
    """

    user_id: str


class StaffVerify(BaseModel):
    """
    Schema for user account verification.

    Attributes:
        user_id (str): The user's ID.
        code (str): The access code for verification.
    """

    user_id: str
    code: str


class StaffLogin(BaseModel):
    """
    Schema for user login requests.

    Attributes:
        email (str): Email address of the user.
        password (str): Password of the user.
    """

    email: str
    password: str


class StaffExistQuery(BaseModel):
    """
    Schema for query parameters to check if a user exists.

    Attributes:
        user_id (str, optional): The unique identifier of the user.
    """
    user_id: str = None


class RefreshToken(BaseModel):
    """
    Schema for request token body

    Attributes:
        refresh_token (str): The unique identifier of the user.
    """

    refresh_token: str
