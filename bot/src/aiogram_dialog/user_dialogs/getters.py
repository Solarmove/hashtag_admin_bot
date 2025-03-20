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
