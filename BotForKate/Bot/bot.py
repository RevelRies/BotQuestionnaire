# файлы проекта
import crud
import fsm_forms
import keyboards

from CBFactories import ThemesCBFactory, AnswerCBFactory
# отдельные импорты
import os
import logging
import asyncio
from magic_filter import F
from dotenv import load_dotenv

# импорты aiogram
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery

load_dotenv()

token = os.getenv('BOTTOKEN')

bot = Bot(token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command(commands=['start']))
async def start_message(message: Message):
    text = 'Привет👋\n' \
           'Я твой личный бот-опросник📋\n' \
           'Сдесь ты можешь добавлять свои вопросы❓, а потом я буду проводить тестирование на их знание\n\n' \
           'ℹ️\n' \
           'Чтобы выбрать тестирование по определенной теме нажми "Выбрать тему"\n' \
           'Чтобы выбрать тестирование по всем темам нажми "Все темы"'

    markup = await keyboards.main_keyboard()


    msg = await message.answer(text=text, reply_markup=markup)
    await message.delete()
    await crud.delete_message(message=msg, time_sec=60)

# обработка кнопок главного меню
# ------------------------------------
@dp.message(Text(text='Выбрать тему'))
async def chose_theme(message: Message):
    text = f'⏬Выберете тему⏬'
    themes = await crud.get_themes()
    markup = await keyboards.themes_inline_keyboard(themes)

    await message.answer(text=text, reply_markup=markup)
    await message.delete()


@dp.message(Text(text='Все темы'))
async def get_random_questions_notheme(message: Message):
    question = await crud.get_random_question()
    answers, text = await crud.get_answers(question=question)

    # text = await crud.answers_output(answers, question)
    markup = await keyboards.get_answers_inline_keyboard(answers)

    await message.answer(text=text, reply_markup=markup)
    await message.delete()

# ------------------------------------

# обработка запросов с инлайн клавиатуры тем
# ------------------------------------
@dp.callback_query(ThemesCBFactory.filter())
async def get_random_questions_theme(query: CallbackQuery, callback_data: ThemesCBFactory):
    question = await crud.get_random_question(theme_pk=callback_data.theme_pk)
    answers, text = await crud.get_answers(question=question)

    # text = await crud.answers_output(answers, question)
    markup = await keyboards.get_answers_inline_keyboard(answers, theme_pk=callback_data.theme_pk)

    await query.message.edit_text(text=text, reply_markup=markup)
# ------------------------------------

# обработка запросов с инлайн клавиатуры ответов
# ------------------------------------
# обработка кнопки главное меню(возврат в главное меню)
@dp.callback_query((AnswerCBFactory.filter(F.action=='main_menu')))
async def bakc_to_main_menu(query: CallbackQuery, calback_data=AnswerCBFactory):
    text = 'Главное меню'
    markup = await keyboards.main_keyboard()

    msg = await query.message.answer(text=text, reply_markup=markup)
    await query.message.delete()
    await crud.delete_message(message=msg, time_sec=30)

# обработка кнопки для получения следующего вопроса
@dp.callback_query(AnswerCBFactory.filter(F.action=='next'))
async def get_next_question(query: CallbackQuery, callback_data=AnswerCBFactory):
    await get_random_questions_theme(query=query, callback_data=callback_data)


# обработка кнопок ответов
@dp.callback_query(AnswerCBFactory.filter(F.action=='answer'))
async def show_answer(query: CallbackQuery, callback_data=AnswerCBFactory):
    if callback_data.val:
        text = 'Правильный ответ✅'
    else:
        text = 'Неправильный ответ❌'

    await query.answer(text=text, show_alert=True)

# ------------------------------------



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())