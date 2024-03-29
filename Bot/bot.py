# файлы проекта
import crud
import fsm_forms
import keyboards
import os

from CBFactories import ThemesCBFactory, AnswerCBFactory
from fsm_forms import AddQuestion
# отдельные импорты
import logging
import asyncio
import os
from magic_filter import F
from dotenv import load_dotenv

# импорты aiogram
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.filters import Command, Text
from aiogram.types import Message, Document, File
from aiogram.filters.callback_data import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()

token = os.getenv('BOTTOKEN')
storage = MemoryStorage()

bot = Bot(token)
dp = Dispatcher(storage=storage)
logging.basicConfig(level=logging.INFO)

@dp.message(Command(commands=['start']))
async def start_message(message: Message):
    text = 'Привет👋\n' \
           'Я твой личный бот-опросник📋\n' \
           'Здесь ты можешь добавлять свои вопросы❓, а потом я буду проводить тестирование на их знание\n\n' \
           'ℹ️\n' \
           'Чтобы выбрать тестирование по определенной теме нажми "Выбрать тему"\n' \
           'Чтобы выбрать тестирование по всем темам нажми "Все темы"'

    markup = await keyboards.main_keyboard()


    msg = await message.answer(text=text, reply_markup=markup)
    await message.delete()
    await crud.delete_message(message=msg, time_sec=30)

# обработка кнопок главного меню
# ------------------------------------
@dp.message(Text(text='Выбрать тему'))
async def chose_theme(message: Message):
    text = f'⏬Выберете тему⏬'
    themes = await crud.get_themes()
    markup = await keyboards.themes_inline_keyboard(themes, add_questions=False)

    await message.answer(text=text, reply_markup=markup)
    await message.delete()


@dp.message(Text(text='Все темы'))
async def get_random_questions_notheme(message: Message):
    question = await crud.get_random_question()
    answers, text = await crud.get_answers(question=question)

    markup = await keyboards.get_answers_inline_keyboard(answers)

    await message.answer(text=text, reply_markup=markup)
    await message.delete()

@dp.message(Text(text='Добавить вопросы'))
async def add_questions(message: Message):
    text = 'Выберите тему к которой хотите добавить вопросы'
    themes = await crud.get_themes()
    markup = await keyboards.themes_inline_keyboard(themes, add_questions=True)

    await message.answer(text=text, reply_markup=markup)
    await message.delete()

# ------------------------------------

# инлайн клавиатуры тем
# ------------------------------------
# обработка запросов с инлайн клавиатуры тем в режиме получения вопросов по этой теме
@dp.callback_query(ThemesCBFactory.filter(F.action=='get_questions'))
async def get_random_questions_theme(query: CallbackQuery, callback_data: ThemesCBFactory):
    question = await crud.get_random_question(theme_pk=callback_data.theme_pk)
    answers, text = await crud.get_answers(question=question)

    markup = await keyboards.get_answers_inline_keyboard(answers, theme_pk=callback_data.theme_pk)

    await query.message.edit_text(text=text, reply_markup=markup)


# обработка запросов с инлайн клавиатуры тем в режиме добавления вопросов по этой теме
@dp.callback_query(ThemesCBFactory.filter(F.action=='add_questions'))
async def add_questions(query: CallbackQuery, callback_data: ThemesCBFactory, state: FSMContext):
    text = 'Чтобы добавить вопросы по этой теме, отправь мне файл в котором вопросы и ответы расположены в следующем формате:\n\n' \
           'Вопрос : правильный ответ : неправильный ответ 1 : неправильный ответ 2 : неправильный ответ 3\n\n' \
           'Важно! Вопрос с ответами на него должны располагаться на одной строке в файле'

    await state.update_data(theme_pk=callback_data.theme_pk)
    await state.set_state(AddQuestion.file)

    msg = await query.message.edit_text(text=text)
    await crud.delete_message(msg, 60)

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


# Обработка фсм состояний
# ------------------------------------
# загрузка файла с вопросами
@dp.message(AddQuestion.file)
async def file_processing(message: Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path

    # скачиваем файл в текущую дерикторию\\User_docs\\ и называем его file.txt
    await bot.download_file(file_path=file_path, destination=f"{os.getcwd()}\\Users_docs\\file.txt")

    # получаем pk выбранной темы и отправляем его в crud для взаимодействия с БД
    data = await state.get_data()
    res = await crud.add_questions(theme_pk=data['theme_pk'])

    # сбрасываем состояние и удаляем все данные
    await state.clear()

    # возвращаем пользователю текстовове сообщение с результатом добавления, удаляем его и отправленный файл
    msg = await message.answer(text=res)
    await message.delete()
    await crud.delete_message(msg, 10)


# ------------------------------------



async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())