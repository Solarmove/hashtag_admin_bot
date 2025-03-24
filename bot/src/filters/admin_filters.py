from typing import Any
from aiogram.filters import Filter
from aiogram.types import Message

from bot.src.utils.unitofwork import UnitOfWork
from configreader import config


class IsAdmin(Filter):
    async def __call__(self, message: Message, uow: UnitOfWork) -> Any:
        return bool(
            await uow.admin_repo.find_one(user_id=message.from_user.id)  # type: ignore
            or message.from_user.id in config.admins  # type: ignore
        )
