import re

from sqlalchemy.orm import validates, relationship
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey

from amht_custom.sqla.models.base import Base


class User(Base):
    __tablename__ = "users"

    # Required fields
    email = Column(String(45), primary_key=True)
    password_hash = Column(String(256), nullable=False)
    zip_code = Column(String(10), nullable=False)

    # Optional account info
    first_name = Column(String(45), nullable=True)
    last_name = Column(String(45), nullable=True)

    # Utility fields
    email_verified = Column(Boolean, nullable=False, default=False)
    needs_password_reset = Column(Boolean, nullable=False, default=False)
    forgot_password_token = Column(String(256), nullable=True)

    @validates("email")
    def validate_email(self, key, email):
        # Simple email validation pattern
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        if not email_pattern.match(email):
            raise ValueError("Invalid email format.")
        return email

    @validates("zip_code")
    def validate_zip_code(self, key, zip_code):
        # Regular expression to match a 5-digit ZIP code or a ZIP+4 code
        zip_code_pattern = re.compile(r"^\d{5}(-\d{4})?$")
        if not zip_code_pattern.match(zip_code):
            raise ValueError("Invalid ZIP code format. Use 5-digit or ZIP+4 format.")
        return zip_code

    def as_dict(self):
        return {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "zip_code": self.zip_code,
            "email_verified": self.email_verified,
            "needs_password_reset": self.needs_password_reset,
        }


class UserSession(Base):
    __tablename__ = "user_session"

    # Required fields
    email = Column(String(45), ForeignKey("users.email"), nullable=False)
    session_token = Column(String(256), primary_key=True)
    last_used = Column(DateTime, nullable=False)

    user = relationship("User", backref="user_session")

    def as_dict(self):
        return {
            "email": self.email,
            "session_token": self.session_token,
            "last_used": self.last_used,
        }
