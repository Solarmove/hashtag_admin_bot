from aiogram.types import User
from aiogram_dialog import DialogManager
from bot.src.utils.unitofwork import UnitOfWork


async def get_data_before_send_message(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    **kwargs,
):
    return {
        "message": dialog_manager.dialog_data["message"],
    }


async def get_phone_number_exist(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    event_from_user: User,
    **kwargs,
):
    user = await uow.user_repo.find_one(
        id=event_from_user.id
    )
    return {
        'phone_number_exist': bool(user.phone_number)
    }

async def get_reg_link(
    dialog_manager: DialogManager,
    uow: UnitOfWork,
    **kwargs,
):
    bar = dialog_manager.start_data['bar']
    return {
        'reg_link': 'google.com' if bar == 'hashtag' else 'yandex.com'
    }

