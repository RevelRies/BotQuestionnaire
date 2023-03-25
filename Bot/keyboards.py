import asyncio

from aiogram.types import KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, InlineKeyboardBuilder
from CBFactories import ThemesCBFactory, AnswerCBFactory

# клавиатура главного меню
async def main_keyboard():
    markup = ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text='Выбрать тему'),
        KeyboardButton(text='Все темы')],
        [KeyboardButton(text='Добавить вопросы')]
        ],
        resize_keyboard=True,
        one_time_keyboard=True)

    return markup

# клавиатура при нажатии на выбор темы
async def themes_inline_keyboard(themes, add_questions: bool | None):
    '''
    функция возвращает инлайн клавиатуру с названиями тем. В случае когда нужно получить вопросы по этой теме
    callback_data возвращает action get_question, а если нужно добавить вопросы action будет add_question
    :param themes: все темы полученные из БД
    :param add_question: параметр который указывает что делать при нажатии на инлайн кнопку с названием темы
    :return: разметку клавиатуры
    '''

    builder = InlineKeyboardBuilder()

    action = 'add_questions' if add_questions else 'get_questions'

    for theme in themes:
        theme_name = theme['name']
        theme_pk = theme['pk']
        builder.add(InlineKeyboardButton(
            text=theme_name,
            callback_data=ThemesCBFactory(theme_pk=theme_pk,
                                          action=action).pack()
        )
    )

    builder.adjust(1)
    murkup = builder.as_markup()
    return murkup

# клавиатура ответов которая выводится после получения вопроса
async def get_answers_inline_keyboard(answers, theme_pk=None):
    builder = InlineKeyboardBuilder()

    # кнопки для возврата в главное меню и следующего вопроса
    builder.add(InlineKeyboardButton(text='Главное меню',
                                     callback_data=AnswerCBFactory(action='main_menu').pack()))

    # если нужен следующий вопрос по определенной тебе то кнопке "Следующий" добавляется theme
    if theme_pk:
        builder.add(InlineKeyboardButton(
            text='Следующий',
            callback_data=AnswerCBFactory(action='next', theme_pk=theme_pk).pack())
                   )
    else:
        builder.add(InlineKeyboardButton(
            text='Следующий',
            callback_data=AnswerCBFactory(action='next').pack())
        )


    # кнопки для выбора ответа
    for indx, answer in enumerate(answers):
        builder.add(InlineKeyboardButton(
            text=f'{indx + 1}',
            callback_data=AnswerCBFactory(action='answer', val=answer['correct']).pack())
        )

    builder.adjust(2, 4)
    markup = builder.as_markup()
    return markup



