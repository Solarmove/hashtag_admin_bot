import operator
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Back, Button, Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format, Multi
from . import states, getters, keyboards, on_clicks

admin_menu_window = Window(
    Const("Виберіть дію:"),
    keyboards.admin_menu_kb,
    state=states.AdminMenu.select_action,
    getter=getters.admin_menu_getter,
)


select_user = Window(
    Const("Виберіть користувача:"),
    keyboards.select_user_kb,
    state=states.SendMessageToUser.select_user,
    getter=getters.get_users_list,
)


def common_write_message_widgets():
    return [
        Multi(
            Const("Напишіть повідомлення:"),
            Format("Номер карти лояльності хештег: {loyalty_card_number_hashtag}"),
            Format("Номер карти лояльності хешрест: {loyalty_card_number_hashrest}"),
        ),
        TextInput(
            id="message",
            on_success=on_clicks.on_write_message,
        ),
    ]


write_message_to_user = Window(
    *common_write_message_widgets(),
    Cancel(Const("Назад")),
    state=states.MessageUser.write_message,
    getter=getters.get_user_info
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
    # Back(Const("Назад")),
    state=states.MessageUser.confirm_send,
    getter=getters.get_data_before_send_message,
)

add_admin_window = Window(
    Const("Відправте айді людини яку ви хочете зробити адміністратором:"),
    TextInput(
        id="admin_id",
        on_success=on_clicks.on_write_admin_id,
    ),
    Cancel(Const("Відмінити")),
    state=states.AddAdmin.write_admin_id,
)

confirm_add_admin_window = Window(
    Const("Ви впевнені, що хочете зробити цю людину адміністратором?"),
    Button(Const("Підтвердити"), id="confirm", on_click=on_clicks.on_confirm_add_admin),
    Back(Const("Назад")),
    state=states.AddAdmin.confirm_add,
)

select_admin_for_delete_window = Window(
    Const("Виберіть адміністратора:"),
    ScrollingGroup(
        Select(
            Format("{item[1]}"),
            id="admin_id",
            items="admins_list",
            on_click=on_clicks.on_select_admin,
            item_id_getter=operator.itemgetter(0),
        ),
        id="admin_list_scroll",
        width=2,
        height=6,
        hide_on_single_page=True,
    ),
    Cancel(Const("Назад")),
    state=states.DeleteAdmin.select_admin,
    getter=getters.get_admins_list,
)


confirm_delete_admin = Window(
    Const("Підтвердьте видалення"),
    Button(
        Const("Підтвердити"), id="confirm", on_click=on_clicks.on_confirm_delete_admin
    ),
    Back(Const("Назад")),
    state=states.DeleteAdmin.confirm_delete,
    getter=getters.get_admins_list,
)
