import config
import crud
import fsm_forms
import logging
import asyncio
import keyboards

from random import shuffle
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.filters import Command, Text
from aiogram.types import Message

token = config.bot_token

bot = Bot(token)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

@dp.message(Command(commands=['start']))
async def start_message(message: Message):
    text = 'Приветственное сообщениие'
    markup = keyboards.main_keyboard()

    await message.answer(text=text, reply_markup=markup)


@dp.message(Text(text='Выбрать тему'))
async def chose_theme(message: Message):
    text = f'Здесь будут темы'
    themes = await crud.get_themes()
    markup = keyboards.themes_inline_keyboard(themes)
    await message.answer(text=text, reply_markup=markup)


@dp.message(Text(text='Все вопросы'))
async def get_random_questions_notheme(message: Message):
    question = await crud.get_random_question(specific=False)
    answers = await crud.get_answers(question=question)

    # засовываем в список res name ответов
    res = [answ['name'] for answ in answers]

    # перемешиваем ответы
    shuffle(res)

    # красивый вывод ответов
    for indx, answ in enumerate(res):
        res[indx] = f'{indx + 1}. {answ}'
    res = '\n'.join(res)

    text = f'Вопрос\n' \
           f'{question["name"]}\n' \
           f'-------------------\n' \
           f'Ответы:\n' \
           f'{res}'

    await message.answer(text=text)










async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())