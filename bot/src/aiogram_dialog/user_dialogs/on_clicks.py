from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.src.db.models.models import UserModel
from bot.src.utils.misc import send_message_to_admin
from bot.src.utils.unitofwork import UnitOfWork


async def on_send_phone_number(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
):
    if not message.contact:
        return
    manager.dialog_data.update(
        phone_number=message.contact.phone_number,
    )
    await manager.next()


async def on_send_loyalty_card_number(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
):
    if not message.text:
        return
    manager.dialog_data.update(
        loyalty_card_number=message.text,
    )
    # TODO: send new user to admins

    await manager.next()


async def on_send_answer(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
):
    manager.dialog_data.update(
        message=message.html_text,
    )
    await manager.next()


async def on_confirm_send_message(
    call: CallbackQuery, widget: Button, manager: DialogManager
):
    message: str = manager.dialog_data["message"]
    admin_id: int = manager.start_data["admin_id"]  # type: ignore
    bot: Bot = manager.middleware_data["bot"]
    uow: UnitOfWork = manager.middleware_data["uow"]
    user_model: UserModel | None = await uow.user_repo.find_one(id=admin_id)
    if not user_model:
        return
    await send_message_to_admin(bot, admin_id, admin_id, user_model.full_name, message)
    await call.answer("Повідомлення надіслано", show_alert=True)
    await manager.done()
