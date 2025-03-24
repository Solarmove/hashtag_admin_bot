from . import windows
from aiogram_dialog import Dialog


dialogs = [
    Dialog(
        windows.send_phone_number,
        windows.send_loyalty_card_number,
        windows.done,
    ),
    Dialog(
        windows.answer_admin,
        windows.confirm_send,
    ),
]
