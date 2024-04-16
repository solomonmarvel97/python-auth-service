from sqlalchemy import Column, String, DateTime, ForeignKey, create_engine
from sqlalchemy import func
import random
from app.helpers.uuid import generate_uuid
from app.config.database import Base
from sqlalchemy.orm import Session


class AccessCode(Base):
    """
    AccessCode model representing the 'access_codes' table in the database.

    Attributes:
        id (String): Unique identifier for the access code record, generated using UUID.
        user_id (String): Foreign key reference to the associated user's ID.
        code (String): The actual access code.
        created_at (DateTime): Timestamp indicating when the access code was created.
    """

    __tablename__ = "access_codes"
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    code = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


def generate_code():
    """
    Generates a 6-digit random access code.

    Returns:
        str: A 6-digit code as a string.

    This function is used to generate a verification or access code.
    The code is random and consists of 6 digits.
    """
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


def save_access_code(db: Session, user_id: str, code: str):
    """
    Saves an access code to the database.

    Args:
        db (Session): The database session.
        user_id (str): The ID of the user for whom the code is generated.
        code (str): The access code to be saved.

    This function creates a new access code record and associates it with a user.
    It then saves this record in the database.
    """
    access_code = AccessCode(user_id=user_id, code=code)
    db.add(access_code)
    db.commit()
