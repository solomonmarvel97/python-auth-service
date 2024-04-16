from sqlalchemy import Column, String, DateTime
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import ARRAY
from app.helpers.uuid import generate_uuid
from app.config.database import Base


class Staff(Base):
    """
    Staff model representing the 'staffs' table in the database.

    Attributes:
        id (String): Unique identifier for the user, generated using UUID.
        email (String): Email address of the user, must be unique.
        username (String): Username of the user, must be unique.
        hashed_password (String): Hashed password for the user.
        roles (ARRAY): List of roles assigned to the user.
        created_at (DateTime): Timestamp indicating when the user record was created.
        updated_at (DateTime): Timestamp indicating when the user record was last updated.
    """

    __tablename__ = "staffs"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    account_status = Column(String, nullable=False, default="pending")
    roles = Column(ARRAY(String), default=lambda: ["Staff"])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
