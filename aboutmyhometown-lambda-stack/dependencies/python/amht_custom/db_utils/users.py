import html
import logging

from amht_custom.sqla.models.tables import User

import bcrypt
from sqlalchemy.orm import Session

logger = logging.getLogger()


def get_user(
    session: Session,
    user_email: str,
) -> User:
    """
    Get a user from the database by email

    Return the user object if found

    Raises ValueError if the user is not found
    """

    user = session.query(User).filter((User.email == user_email)).first()

    if user is None:
        raise ValueError("User not found!")

    return user


def check_password(
    session: Session,
    user_email: str,
    password_rawstring: str,
) -> bool:
    """
    Get a user from the database by email

    Return true if the password is correct, false otherwise

    Raises ValueError if the user is not found
    """

    user = get_user(session=session, user_email=user_email)

    if user is None:
        raise ValueError("User not found!")

    if not bcrypt.checkpw(password_rawstring.encode("utf-8"), user.password_hash):
        return False

    return True


def modify_user(
    session: Session,
    email: str,
    password_rawstring: str = None,
    zip_code: str = None,
    first_name: str = None,
    last_name: str = None,
    email_verified: bool = False,
    needs_password_reset: bool = False,
    forgot_password_token: str = None,
):
    """
    Modify a user in the database

    return the user object if successful, raise ValueError otherwise
    """
    user = get_user(session, email)

    if password_rawstring is not None:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_rawstring.encode("utf-8"), salt)
        user.password_hash = hashed_password

    if zip_code is not None:
        user.zip_code = html.escape(zip_code)

    if first_name is not None:
        user.first_name = html.escape(first_name)

    if last_name is not None:
        user.last_name = html.escape(last_name)

    if email_verified is not None:
        user.email_verified = email_verified

    if needs_password_reset is not None:
        user.needs_password_reset = needs_password_reset

    if forgot_password_token is not None:
        user.forgot_password_token = forgot_password_token

    session.commit()

    return user


def create_user(
    session: Session,
    email: str,
    password_rawstring: str,
    zip_code: str,
    first_name: str = None,
    last_name: str = None,
    email_verified: bool = False,
    needs_password_reset: bool = False,
    forgot_password_token: str = None,
) -> User:
    """
    Create a new user in the database

    return the user object if successful, raise ValueError otherwise
    """

    user_email_sanitized = html.escape(email) if email else None
    zip_code_sanitized = html.escape(zip_code) if zip_code else None
    first_name_sanitized = html.escape(first_name) if first_name else None
    last_name_sanitized = html.escape(last_name) if last_name else None

    if (
        user_email_sanitized
        and session.query(User).filter((User.email == user_email_sanitized)).first()
        is not None
    ):
        raise ValueError("User already exists. Please use a different email.")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_rawstring.encode("utf-8"), salt)

    try:
        new_user = User(
            first_name=first_name_sanitized,
            last_name=last_name_sanitized,
            email=user_email_sanitized,
            password_hash=hashed_password,
            zip_code=zip_code_sanitized,
            email_verified=email_verified,
            needs_password_reset=needs_password_reset,
            forgot_password_token=forgot_password_token,
        )
    except ValueError as error:
        raise ValueError(str(error))

    session.add(new_user)
    session.commit()

    return new_user
