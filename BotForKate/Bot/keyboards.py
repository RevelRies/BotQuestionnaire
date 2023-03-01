import asyncio

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, InlineKeyboardBuilder
from CBFactories import ThemesCBFactory, AnswerCBFactory

# клавиатура главного меню
async def main_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text='Выбрать тему'),
        KeyboardButton(text='Все вопросы')]],
        resize_keyboard=True,
        one_time_keyboard=True)

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

    # кнопки для возврата в главное меню и следующего вопроса
    builder.add(InlineKeyboardButton(text='Главное меню',
                                     callback_data=AnswerCBFactory(action='main_menu').pack()),
                InlineKeyboardButton(text='Следующий',
                                     callback_data=AnswerCBFactory(action='next').pack())
                )


    # кнопки для выбора ответа
    for indx, answer in enumerate(answers):
        builder.add(InlineKeyboardButton(
            text=f'{indx + 1}',
            callback_data=AnswerCBFactory(action='get_answer', val=answer['correct']).pack())
        )

    builder.adjust(2, 4)
    markup = builder.as_markup()
    return markup

