from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Next, RequestContact
from aiogram_dialog.widgets.text import Const, Format, Multi

from . import states, keyboards, getters, on_clicks

send_phone_number = Window(
    Const("Введіть номер телефону щоб отримати кальян"),
    MessageInput(
        func=on_clicks.on_send_phone_number, content_types=ContentType.CONTACT
    ),
    RequestContact(Const("Відправити номер телефону")),
    Next(Const("Номер не змінився"), when='phone_number_exist'),
    state=states.CreateNewUser.send_phone_number,
    getter=getters.get_phone_number_exist,
)

send_loyalty_card_number = Window(
    Multi(
    Const(
        "Введіть номер карти лояльності\n\n"
        "<i>Якщо у вас її ще немає - створити можна за цим посиланням</i>"
    ),
        Format(
            "{reg_link}"
        )
    ),
    MessageInput(
        func=on_clicks.on_send_loyalty_card_number, content_types=ContentType.TEXT
    ),
    state=states.CreateNewUser.send_loyalty_card_number,
    getter=getters.get_reg_link
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
