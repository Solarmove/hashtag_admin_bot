from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Select

from bot.src.aiogram_dialog.admin_dialogs import states
from bot.src.utils.misc import send_message, send_message_to_user
from bot.src.utils.unitofwork import UnitOfWork


async def on_select_user(
    call: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
):
    await manager.start(
        states.MessageUser.write_message, data={"user_id": int(item_id)}
    )


async def on_write_message(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    manager.dialog_data.update(
        message=message.html_text,
    )
    await manager.next()


async def on_confirm_send(
    call: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    start_data = manager.start_data
    user_id = manager.dialog_data.get("user_id", start_data.get("user_id", 0))  # type: ignore
    message = manager.dialog_data["message"]
    bot: Bot = manager.middleware_data["bot"]
    await send_message_to_user(bot, user_id, message)
    await call.answer("Повідомлення надіслано", show_alert=True)
    await manager.done()


async def on_write_admin_id(
    message: Message,
    widget: ManagedTextInput,
    manager: DialogManager,
    message_text: str,
):
    uow: UnitOfWork = manager.middleware_data["uow"]
    user_exist = await uow.user_repo.find_one(id=int(message_text))
    if not user_exist:
        return await message.answer("Користувача з таким айді не існує")
    if await uow.admin_repo.find_one(user_id=int(message_text)):
        return await message.answer("Користувач вже є адміністратором")
    manager.dialog_data.update(
        user_id=int(message_text),
    )

    await manager.next()


async def on_confirm_add_admin(
    call: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    user_id = manager.dialog_data.get("user_id", 0)  # type: ignore
    uow: UnitOfWork = manager.middleware_data["uow"]
    await uow.admin_repo.add_one({"id": None, "user_id": user_id})
    await uow.commit()
    await call.answer("Користувача зроблено адміністратором", show_alert=True)
    await manager.done()


async def on_select_admin(
    call: CallbackQuery,
    widget: Select,
    manager: DialogManager,
    item_id: str,
):
    manager.dialog_data.update(
        admin_id=int(item_id),
    )
    await manager.next()


async def on_confirm_delete_admin(
    call: CallbackQuery,
    widget: Button,
    manager: DialogManager,
):
    admin_id = manager.dialog_data.get("admin_id", 0)  # type: ignore
    uow: UnitOfWork = manager.middleware_data["uow"]
    await uow.admin_repo.delete_one(id=admin_id)
    await uow.commit()
    await call.answer("Адміністратора видалено", show_alert=True)
    await manager.done()
