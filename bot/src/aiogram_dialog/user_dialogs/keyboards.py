from aiogram_dialog.widgets.kbd import Back, Button, Group
from aiogram_dialog.widgets.text import Const



from . import on_clicks

on_confirm_send_message = Group(
    Button(
        Const("Підтвердити"),
        id="confirm",
        on_click=on_clicks.on_confirm_send_message,
    ),
    Back(Const("Назад")),
)
