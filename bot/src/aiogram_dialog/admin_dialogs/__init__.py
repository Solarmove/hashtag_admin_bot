from . import windows
from aiogram_dialog import Dialog


dialogs = [
    Dialog(windows.user_main_menu_window),
    Dialog(
        windows.select_group_window_for_create_reg_task,
        windows.select_type_of_task_window,
        windows.select_frequency_window,
        windows.enter_task_name_window,
        windows.confirm_create_task_window,
    ),
    Dialog(
        windows.select_group_for_show_reg_tasks_window,
        windows.show_regular_tasks_window,
    ),
    Dialog(windows.confirm_delete_reg_task_window),
    Dialog(
        windows.select_group_for_show_tasks_window,
        windows.show_user_tasks_window,
    ),
    Dialog(windows.task_action_window),
    Dialog(
        windows.select_reason_for_delete_window,
        windows.confirm_delete_task_window,
    ),
    Dialog(windows.enter_new_task_text_window),
    Dialog(windows.select_new_deadline_window),
]
