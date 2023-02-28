from aiogram.filters.callback_data import CallbackData

class ThemesCBFactory(CallbackData, prefix='themes'):
    theme: str