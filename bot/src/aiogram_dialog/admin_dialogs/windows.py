import datetime
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    CalendarConfig,
    Cancel,
    CurrentPage,
    NextPage,
    NumberedPager,
    PrevPage,
    Start,
    SwitchTo,
    Row,
)
from aiogram_dialog.widgets.text import Const, Format, List, Multi
from magic_filter import F

from bot.src.aiogram_dialog.user_dialogs import getters, states, keyboards, on_clicks
from bot.src.utils.castom_calendar import CustomCalendar
from bot.src.utils.enum import TaskType

