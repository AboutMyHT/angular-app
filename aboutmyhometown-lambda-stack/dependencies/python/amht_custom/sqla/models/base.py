"""Base objects for SQLAlchemy implementation"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base. Used for implementation-wide ORM changes"""
