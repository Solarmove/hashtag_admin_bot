from aiogram.fsm.state import State, StatesGroup


class AdminMenu(StatesGroup):
    select_action = State()


class SendMessageToUser(StatesGroup):
    select_user = State()



class MessageUser(StatesGroup):
    write_message = State()
    confirm_send = State()



class AddAdmin(StatesGroup):
    write_admin_id = State()
    confirm_add = State()


class DeleteAdmin(StatesGroup):
    select_admin = State()
    confirm_delete = State()
