# файлы проекта
import config
import crud
import fsm_forms
import keyboards

from CBFactories import ThemesCBFactory
# отдельные импорты
import logging
import asyncio

# импорты aiogram
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackQuery

token = config.bot_token

bot = Bot(token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command(commands=['start']))
async def start_message(message: Message):
    text = 'Приветственное сообщениие'
    markup = await keyboards.main_keyboard()

    await message.answer(text=text, reply_markup=markup)


# обработка кнопок главного меню
# ------------------------------------
@dp.message(Text(text='Выбрать тему'))
async def chose_theme(message: Message):
    text = f'Здесь будут темы'
    themes = await crud.get_themes()
    markup = await keyboards.themes_inline_keyboard(themes)
    await message.answer(text=text, reply_markup=markup)


@dp.message(Text(text='Все вопросы'))
async def get_random_questions_notheme(message: Message):
    question = await crud.get_random_question(specific=False)
    answers = await crud.get_answers(question=question)

    text = await crud.answers_output(answers, question)
    markup = await keyboards.get_answers_inline_keyboard(answers)

    await message.answer(text=text, reply_markup=markup)

# ------------------------------------

# обработка запросов с инлайн клавиатуры тем
# ------------------------------------
@dp.callback_query(ThemesCBFactory.filter())
async def get_random_questions_theme(query: CallbackQuery, callback_data: ThemesCBFactory):
    question = await crud.get_random_question(specific=True, theme=callback_data.theme)
    answers = await crud.get_answers(question=question)

    text = await crud.answers_output(answers, question)
    markup = await keyboards.get_answers_inline_keyboard(answers)

    await query.message.edit_text(text=text, reply_markup=markup)
# ------------------------------------





async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())