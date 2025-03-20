from bot.src.db.models.models import AdminModel, UserModel
from bot.src.utils.repository import SQLAlchemyRepository


class UserRepo(SQLAlchemyRepository):
    model = UserModel


class AdminRepo(SQLAlchemyRepository):
    model = AdminModel
