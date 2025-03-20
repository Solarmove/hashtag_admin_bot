from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.text import Const, Format, Multi
from . import states, getters, keyboards, on_clicks

admin_menu_window = Window(
    Const("Виберіть дію:"),
    keyboards.admin_menu_kb,
    state=states.AdminMenu.select_action,
)


select_user = Window(
    Const("Виберіть користувача:"),
    keyboards.select_user_kb,
    state=states.SendMessageToUser.select_user,
    getter=getters.get_users_list,
)


def common_write_message_widgets():
    return [
        Const("Напишіть повідомлення:"),
        TextInput(
            id="message",
            on_success=on_clicks.on_write_message,
        ),
    ]


write_message_to_user = Window(
    *common_write_message_widgets(),
    state=states.MessageUser.write_message,
)


def common_confirm_send_message_widgets():
    return [
        Multi(
            Const("Ви впевнені, що хочете надіслати це повідомлення?\n"),
            Format("Користувач: {user_full_name}"),
            Format("Повідомлення: {message}"),
        ),
        keyboards.on_confirm_send_message(),
    ]


confirm_send_message_window = Window(
    *common_confirm_send_message_widgets(),
    state=states.MessageUser.confirm_send,
    getter=getters.get_data_before_send_message,
)
