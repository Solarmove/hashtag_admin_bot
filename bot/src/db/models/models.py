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
    loyalty_card_number = mapped_column(VARCHAR(255), nullable=True)


class AdminModel(Base):
    __tablename__ = "admins"

    id = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    user_id = mapped_column(INTEGER, ForeignKey("users.id"), nullable=False)
