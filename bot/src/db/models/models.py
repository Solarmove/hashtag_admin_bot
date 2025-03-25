from sqlalchemy import BOOLEAN, ForeignKey,  func, VARCHAR
from sqlalchemy.dialects.sqlite import INTEGER
from sqlalchemy.orm import mapped_column

from bot.src.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = mapped_column(INTEGER, primary_key=True, autoincrement=False)
    username = mapped_column(VARCHAR(255), nullable=False)
    full_name = mapped_column(VARCHAR(255), nullable=False)
    phone_number = mapped_column(VARCHAR(255), nullable=True)
    loyalty_card_number_hash_tag = mapped_column(VARCHAR(255), nullable=True)
    loyalty_card_number_hash_rest = mapped_column(VARCHAR(255), nullable=True)


class AdminModel(Base):
    __tablename__ = "admins"

    id = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id = mapped_column(INTEGER, ForeignKey("users.id"), nullable=False)


class DeepLink(Base):
    __tablename__ = 'deep_links'

    id = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    phone_number = mapped_column(VARCHAR(255), nullable=False)
    code = mapped_column(VARCHAR(255), nullable=False)
    bar = mapped_column(VARCHAR(255), nullable=False)
    used = mapped_column(BOOLEAN, nullable=False, default=False)

