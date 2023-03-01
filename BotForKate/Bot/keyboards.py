import asyncio

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from CBFactories import ThemesCBFactory, AnswerCBFactory

# клавиатура главного меню
async def main_keyboard():
    builder = ReplyKeyboardBuilder()
    btn1 = KeyboardButton(text='Выбрать тему')
    btn2 = KeyboardButton(text='Все вопросы')

    builder.add(btn1, btn2)
    builder.adjust(2)
    markup = builder.as_markup(resize_keyboard=True)
    return markup

# клавиатура при нажатии на выбор темы
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

# клавиатура ответов которая выводится после получения вопроса
async def get_answers_inline_keyboard(answers):
    builder = InlineKeyboardBuilder()
    for indx, answer in enumerate(answers):
        builder.add(InlineKeyboardButton(
            text=f'{indx + 1}',
            callback_data=AnswerCBFactory(action='get_answer', val=answer['correct']).pack())
        )

    markup = builder.as_markup()
    return markup


# обычная клавиатура меню ответов на вопросы
async def get_answers_keyboard():
    builder = ReplyKeyboardBuilder()
    btn1 = KeyboardButton(text='Главное меню')
    btn2 = KeyboardButton(text='Следующий вопрос')

    builder.add(btn1, btn2)
    builder.adjust(2)
    markup = builder.as_markup(resize_keyboard=True)
    return markup