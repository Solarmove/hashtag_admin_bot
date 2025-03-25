from typing import Literal

from aiogram import F, Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.payload import decode_payload
from aiogram_dialog import DialogManager
from bot.src.aiogram_dialog.admin_dialogs.states import AdminMenu, MessageUser
from bot.src.aiogram_dialog.user_dialogs.states import AnswerOnMessage, CreateNewUser
from bot.src.filters.admin_filters import IsAdmin
from bot.src.utils.misc import add_user
from bot.src.utils.unitofwork import UnitOfWork

router = Router()


@router.callback_query(F.data.startswith("answer:"))
async def answer_admins_handler(call: CallbackQuery, dialog_manager: DialogManager):
    call_data = str(call.data)
    answer_to = call_data.split(":")[1]
    if answer_to == "admins":
        await dialog_manager.start(AnswerOnMessage.send_message)
    elif answer_to.isdigit():
        await dialog_manager.start(
            MessageUser.write_message, data={"user_id": int(answer_to)}
        )


@router.message(Command("admin", "a"), IsAdmin())
async def admin_start_handler(
    message: Message, uow: UnitOfWork, dialog_manager: DialogManager
):
    if not message.from_user:
        return
    await add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
        uow,
    )

    await dialog_manager.start(AdminMenu.select_action)


@router.message(CommandStart(deep_link=True))
async def start_from_sms_handler(
    message: Message, command: CommandObject, uow: UnitOfWork, dialog_manager: DialogManager
):
    args = command.args
    payload = decode_payload(args) # type: ignore
    if not payload.startswith('sms_'):
        return
    if not message.from_user:
        return
    code = payload.split("_")[1]
    if not code.isdigit():
        return
    bar: Literal['hashtag', 'hashrest'] = payload.split("_")[2] # noqa
    code = int(code)
    stored_link = await uow.deep_link_repo.find_one(code=code, bar=bar)
    if not stored_link or stored_link.used is True:
        return

    await add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.full_name,
        uow,
    )
    await dialog_manager.start(
        CreateNewUser.send_phone_number,
        data={
            "deep_link_id": stored_link.id,
            'bar': bar,
            'code': code,
            'deep_link_phone_number': stored_link.phone_number
        },

    )


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
