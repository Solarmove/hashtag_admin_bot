from . import windows
from aiogram_dialog import Dialog


dialogs = [
    Dialog(
        windows.admin_menu_window,
    ),
    Dialog(
        windows.select_user,
    ),
    Dialog(
        windows.write_message_to_user,
        windows.confirm_send_message_window,
    ),
    Dialog(windows.add_admin_window, windows.confirm_add_admin_window),
    Dialog(windows.select_admin_for_delete_window, windows.confirm_delete_admin),
]
