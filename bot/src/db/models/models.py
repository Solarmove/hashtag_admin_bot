from sqlalchemy import BIGINT, BOOLEAN, ForeignKey, func, VARCHAR
from sqlalchemy.dialects.postgresql import ENUM, TIME, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, Relationship

from bot.src.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username = mapped_column(VARCHAR(255), nullable=False)
    full_name = mapped_column(VARCHAR(255), nullable=False)
    phone_number = mapped_column(VARCHAR(255), nullable=True)
    loyalty_card_number = mapped_column(VARCHAR(255), nullable=True)


class AdminModel(Base):
    __tablename__ = "admins"

    id = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    user_id = mapped_column(BIGINT, ForeignKey("users.id"), nullable=False)
