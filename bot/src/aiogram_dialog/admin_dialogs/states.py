from aiogram.fsm.state import State, StatesGroup


class AdminMenu(StatesGroup):
    select_action = State()


class SendMessageToUser(StatesGroup):
    select_user = State()



class MessageUser(StatesGroup):
    write_message = State()
    confirm_send = State()
