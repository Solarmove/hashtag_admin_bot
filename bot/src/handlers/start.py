from aiogram import F, Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from bot.src.filters.admin_filters import IsAdmin
from bot.src.utils.misc import add_user
from bot.src.utils.unitofwork import IUnitOfWork, UnitOfWork

router = Router()


@router.message(CommandStart())
async def start_from_sms_handler(
    message: Message, command: CommandObject, uow: UnitOfWork
):
    if not message.from_user:
        return
    await add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
        uow,
    )
    if not command.args or command.args == "source_sms":
        return
    await message.answer("Ви зайшли по sms посиланню")


@router.message(CommandStart(), IsAdmin())
async def admin_start_handler(message: Message, uow: UnitOfWork): ...


@router.message(CommandStart())
async def start_handler(message: Message, uow: UnitOfWork):
    if not message.from_user:
        return

    await add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
        uow,
    )
