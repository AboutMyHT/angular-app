from sqlalchemy import String, Column

from amht_custom.sqla.models.base import Base


class User(Base):
    __tablename__ = "users"
    email = Column(String(45), primary_key=True)
    name = Column(String(45), nullable=False)
    password_hash = Column(String(256), nullable=False)
