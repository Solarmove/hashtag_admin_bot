from typing import Sequence
from aiogram.types import user
from aiogram_dialog import DialogManager

from bot.src.db.models.models import UserModel
from bot.src.utils.unitofwork import UnitOfWork


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
    user_id = dialog_manager.dialog_data.get("user_id")
    user_model: UserModel | None = await uow.user_repo.find_one(id=user_id)
    if not user_model:
        return {}
    return {
        "user_full_name": user_model.full_name,
        "message": dialog_manager.dialog_data["message"],
    }
