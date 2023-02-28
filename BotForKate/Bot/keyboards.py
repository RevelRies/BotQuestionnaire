import asyncio

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from CBFactories import ThemesCBFactory


async def main_keyboard():
    builder = ReplyKeyboardBuilder()
    btn1 = KeyboardButton(text='Выбрать тему')
    btn2 = KeyboardButton(text='Все вопросы')

    builder.add(btn1, btn2)
    builder.adjust(2)
    markup = builder.as_markup(resize_keyboard=True)
    return markup

async def themes_inline_keyboard(themes):
    builder = InlineKeyboardBuilder()
    for theme in themes:
        theme_name = theme['name']
        builder.add(InlineKeyboardButton(
            text=theme_name,
            callback_data=ThemesCBFactory(theme=theme_name).pack()
        )
    )

    builder.adjust(1)
    murkup = builder.as_markup()
    return murkup