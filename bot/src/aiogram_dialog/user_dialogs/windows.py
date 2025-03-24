from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format, Multi

from . import states, keyboards, getters, on_clicks

send_phone_number = Window(
    Const("Введіть номер телефону щоб отримати кальян"),
    MessageInput(
        func=on_clicks.on_send_phone_number, content_types=ContentType.CONTACT
    ),
    state=states.CreateNewUser.send_phone_number,
)

send_loyalty_card_number = Window(
    Const(
        "Введіть номер карти лояльності\n\n<i>Якщо у вас її ще немає - створи за цим посиланням</i>"
    ),
    MessageInput(
        func=on_clicks.on_send_loyalty_card_number, content_types=ContentType.TEXT
    ),
    state=states.CreateNewUser.send_loyalty_card_number,
)

done = Window(
    Const("Ви успішно зареєструвались. Наші адміністратори з вами зв'яжуться."),
    state=states.CreateNewUser.done,
)


answer_admin = Window(
    Const("Введіть ваше повідомлення:"),
    MessageInput(func=on_clicks.on_send_answer, content_types=ContentType.TEXT),
    Cancel(Const("Відмінити")),
    state=states.AnswerOnMessage.send_message,
)


confirm_send = Window(
    Multi(
        Const("Ви впевнені, що хочете надіслати це повідомлення?\n"),
        Format  ("Повідомлення: {message}"),
    ),
    keyboards.on_confirm_send_message,
    state=states.AnswerOnMessage.confirm_send,
    getter=getters.get_data_before_send_message,
)
