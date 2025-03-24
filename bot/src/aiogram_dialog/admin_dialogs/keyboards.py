import operator
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Group,
    Row,
    ScrollingGroup,
    Select,
    Start,
)
from aiogram_dialog.widgets.text import Const, Format
from . import states, on_clicks

admin_menu_kb = Group(
    Start(
        Const("Написати повідомлення користувачу"),
        id="send_message_to_user",
        state=states.SendMessageToUser.select_user,
    ),
    Row(
        Start(
            Const("Додати адміна"),
            id="add_admin",
            state=states.AddAdmin.write_admin_id,
        ),
        Start(
            Const("Видалити адміна"),
            id="exit",
            state=states.DeleteAdmin.select_admin
        ),
        when='is_root_admin',
    ),
)


select_user_kb = Group(
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="user_id",
            on_click=on_clicks.on_select_user,
            item_id_getter=operator.itemgetter(0),
            items="users_list",
        ),
        id="users_scroll",
        width=2,
        height=6,
        hide_on_single_page=True,
    ),
    Cancel(Const("Відмінити")),
)


def on_confirm_send_message():
    return Group(
        Button(
            Const("Підтвердити"),
            id="confirm",
            on_click=on_clicks.on_confirm_send,
        ),
        Back(Const("Назад")),
    )
