from sqlalchemy import delete
from bot.src.db.models.models import AdminModel, UserModel
from bot.src.utils.repository import SQLAlchemyRepository


class UserRepo(SQLAlchemyRepository):
    model = UserModel


class AdminRepo(SQLAlchemyRepository):
    model = AdminModel

    async def delete_one(self, **filter_by):
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
        
