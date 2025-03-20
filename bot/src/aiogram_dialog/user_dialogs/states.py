from aiogram.fsm.state import State, StatesGroup


class CreateNewUser(StatesGroup):
    """Состояния для создания нового пользователя"""

    send_phone_number = State()
    send_loyalty_card_number = State()
    done = State()


class AnswerOnMessage(StatesGroup):
    """Состояния для ответа на сообщение"""

    send_answer = State()
