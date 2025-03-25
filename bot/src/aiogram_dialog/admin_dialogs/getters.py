from typing import Sequence
from aiogram import Bot
from aiogram.types import User
from aiogram_dialog import DialogManager

from bot.src.db.models.models import AdminModel, UserModel
from bot.src.utils.unitofwork import UnitOfWork
from configreader import config


async def admin_menu_getter(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    event_from_user: User,
    **kwargs,
):
    return {"is_root_admin": event_from_user.id in config.admins}


async def get_users_list(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    **kwargs,
):
    users_model_list: Sequence[UserModel] = await uow.user_repo.find_all()
    return {
        "users_list": [
            (user_model.id, user_model.full_name) for user_model in users_model_list
        ]
    }


async def get_data_before_send_message(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    **kwargs,
):
    user_id = dialog_manager.start_data.get("user_id") # type: ignore
    user_model: UserModel | None = await uow.user_repo.find_one(id=user_id)
    print(user_model)
    if not user_model:
        return {}
    return {
        "user_full_name": user_model.full_name,
        "message": dialog_manager.dialog_data["message"],
    }


async def get_admins_list(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    bot: Bot,
    **kwargs,
):
    admins_model_list: Sequence[AdminModel] = await uow.admin_repo.find_all()
    return {
        "admins_list": [
            (admin_model.id, (await bot.get_chat(admin_model.user_id)).full_name)
            for admin_model in admins_model_list
        ]
    }


async def get_user_info(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    **kwargs,
):
    user_id = dialog_manager.start_data.get("user_id") # type: ignore
    user_model: UserModel | None = await uow.user_repo.find_one(id=user_id)
    if not user_model:
        return {}
    return {
        "user_full_name": user_model.full_name,
        "loyalty_card_number_hashtag": user_model.loyalty_card_number_hash_tag,
        "loyalty_card_number_hashrest": user_model.loyalty_card_number_hash_rest,
    }