"""
    Purpose: This module contains common operations for managing, validating, and generating user sessions
    Requirements: 3.3.x; 5.x
"""
import logging
from uuid import UUID, uuid4
from datetime import datetime, timedelta

from amht_custom.sqla.models.tables import UserSession

from sqlalchemy.orm import Session

logger = logging.getLogger()

HOURS_TO_KEEP_SESSIONS = 24


def clean_sessions(session: Session) -> None:
    """
    Remove all sessions that have not been used in the last 24 hours
    """

    session.query(UserSession).filter(
        UserSession.last_used < datetime.now() - timedelta(hours=HOURS_TO_KEEP_SESSIONS)
    ).delete()
    session.commit()


def validate_token(session: Session, session_token: UUID) -> bool:
    """
    Accept a session token

    Return True if the token is valid and has been used in the last 24 hours
    """

    token = (
        session.query(UserSession)
        .filter((UserSession.session_token == session_token))
        .first()
    )

    if token is not None and token.last_used > datetime.now() - timedelta(
        hours=HOURS_TO_KEEP_SESSIONS
    ):
        token.last_used = datetime.now()
        session.commit()
        return True

    return False


def get_user_session(session: Session, session_token: UUID) -> UserSession:
    """
    Accept a session token

    Return the user associated with the token
    """

    user_session = (
        session.query(UserSession)
        .filter((UserSession.session_token == session_token))
        .first()
    )

    if user_session is None:
        raise ValueError("User Session not found!")

    return user_session


def generate_session_token(session: Session, user_email: str) -> UUID:
    """
    Generate a new session token for a user

    Return the session token
    """

    clean_sessions(session)

    session_token = uuid4()

    new_session = UserSession(
        email=user_email,
        session_token=session_token,
        last_used=datetime.now(),
    )

    session.add(new_session)
    session.commit()

    return session_token
