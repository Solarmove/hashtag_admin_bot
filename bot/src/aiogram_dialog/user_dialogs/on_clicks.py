from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from bot.src.db.models.models import UserModel
from bot.src.utils.misc import send_message, send_message_to_admin
from bot.src.utils.unitofwork import UnitOfWork


async def on_send_phone_number(
    message: Message,
    widget: MessageInput,
    manager: DialogManager,
):
    if not message.contact:
        await message.answer("Відправте номер телефону")
        return
    if message.contact.phone_number != manager.start_data["deep_link_phone_number"]:
        await message.answer('Номер телефону не співпадає з вказаним')
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
    uow: UnitOfWork = manager.middleware_data["uow"]
    bot: Bot = manager.middleware_data["bot"]
    admins = await uow.admin_repo.find_all()
    phone_number = manager.dialog_data["phone_number"]
    loyalty_card_number = manager.dialog_data["loyalty_card_number"]
    bar = manager.start_data["bar"]

    await uow.user_repo.edit_one(
        id=message.from_user.id,
        data={
            "loyalty_card_number_hash_tag": loyalty_card_number
            if bar == "hashtag"
            else None,
            "loyalty_card_number_hash_rest": loyalty_card_number
            if bar == "hashrest"
            else None,
            "phone_number": phone_number,
        },
    )
    await uow.deep_link_repo.edit_one(
        id=manager.start_data['deep_link_id'],
        data={
            'used': True,
        }
    )
    await uow.commit()

    for admin in admins:
        await send_message(
            bot,
            admin.user_id,
            f"Новий користувач ({message.from_user.username or message.from_user.full_name}) зареєстрований в системі.\n\n" # type: ignore
            f"Номер телефону: {phone_number}\n"
            f"Номер лояльності: {loyalty_card_number}",
        )

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
    bot: Bot = manager.middleware_data["bot"]
    uow: UnitOfWork = manager.middleware_data["uow"]
    admins = await uow.admin_repo.find_all()
    user_model: UserModel | None = await uow.user_repo.find_one(id=call.from_user.id)
    if not user_model:
        return
    for admin in admins:
        await send_message_to_admin(
            bot, admin.user_id, call.from_user.id, user_model.full_name, message
        )
    await call.answer("Повідомлення надіслано", show_alert=True)
    await manager.done()
