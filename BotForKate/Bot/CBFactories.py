from aiogram.filters.callback_data import CallbackData
from typing import Optional

class ThemesCBFactory(CallbackData, prefix='themes'):
    theme: str


class AnswerCBFactory(CallbackData, prefix='answers'):
    action: str
    val: Optional[bool]