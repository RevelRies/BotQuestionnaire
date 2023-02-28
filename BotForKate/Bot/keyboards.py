from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
def main_keyboard():
    builder = ReplyKeyboardBuilder()
    btn1 = KeyboardButton(text='Выбрать тему')
    btn2 = KeyboardButton(text='Все вопросы')

    builder.add(btn1, btn2)
    builder.adjust(2)
    markup = builder.as_markup(resize_keyboard=True)
    return markup

def themes_inline_keyboard(themes):
    builder = InlineKeyboardBuilder()
    for theme in themes:
        builder.add(InlineKeyboardButton(text=theme, callback_data=f'theme_{theme}'))

    builder.adjust(1)
    murkup = builder.as_markup()
    return murkup