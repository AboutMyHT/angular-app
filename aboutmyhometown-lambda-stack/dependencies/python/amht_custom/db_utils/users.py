import html
import logging

from amht_custom.sqla.models.tables import User

import bcrypt
from sqlalchemy.orm import Session

logger = logging.getLogger()


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
):
    """
    Execute the query on the MySQL database
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
    hashed_password = bcrypt.hashpw(password_rawstring, salt)

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

    user_str = {
        "name": f"{new_user.first_name} {new_user.last_name}",
        "email": new_user.email,
        "zip_code": new_user.zip_code,
    }

    return user_str
