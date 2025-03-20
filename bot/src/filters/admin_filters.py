from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message

from bot.src.utils.unitofwork import UnitOfWork


class IsAdmin(Filter):
    async def __call__(self, message: Message, uow: UnitOfWork) -> Any:
        return bool(await uow.admin_repo.find_one(user_id=message.from_user.id)) # type: ignore
