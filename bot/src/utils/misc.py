import logging
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import InlineKeyboardButton, ReplyMarkupUnion
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.link import create_tg_link

from bot.src.utils.unitofwork import UnitOfWork


async def get_user_url(username: str | None, user_id: int, full_name: str):
    """Получает ссылку на пользователя"""
    if username:
        return f"@{username}"
    user_url = create_tg_link("user", id=user_id)
    return f"<a href='{user_url}'>{full_name}</a>"


async def add_user(user_id: int, username: str | None, full_name: str, uow: UnitOfWork):
    """Добавляет пользователя в базу данных"""

    user_exist = await uow.user_repo.find_one(id=user_id)
    if not user_exist:
        await uow.user_repo.add_one(
            {
                "id": user_id,
                "username": username,
                "full_name": full_name,
            }
        )
        await uow.commit()


async def send_message(
    bot: Bot, chat_id: int, text: str, keyboard: ReplyMarkupUnion | None = None
):
    """Отправляет сообщение"""
    try:
        await bot.send_message(chat_id, text, reply_markup=keyboard)
    except TelegramForbiddenError as er:
        logging.info("TelegramForbiddenError: %s", er)
        pass
    except TelegramBadRequest as er:
        logging.info("TelegramBadRequest: %s", er)
        pass
    except Exception as er:
        logging.error("Exception: %s", er)


async def send_message_to_user(bot: Bot, user_id: int, text: str):
    """Отправляет сообщение пользователю"""
    text = f"📬 Повідомлення від адміністратора:\n\n<i>{text}</i>"
    await send_message(bot, user_id, text)


async def send_message_to_admin(
    bot: Bot, admin_id: int, user_id: int, full_name: str, text: str
):
    """Отправляет сообщение администратору"""
    user_link = await get_user_url(None, user_id, full_name)
    kb = InlineKeyboardBuilder()
    kb.add(
        InlineKeyboardButton(
            text="Профіль користувача",
            url=user_link,
        )
    )
    text = f"📬 Повідомлення від користувача <b>{full_name}</b>:\n\n<i>{text}</i>"
    await send_message(bot, admin_id, text, keyboard=kb.as_markup())
