import aiohttp
import asyncio
from random import choice, shuffle

# получение всех тем
async def get_themes():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/themes/') as response:

            themes = await response.json()
            return themes


# получение рандомного вопроса по всем темам или по определенной
# если нужна определенная тема то атрибут theme != None
async def get_random_question(theme_pk=None):
    # если надо получить вопрос по всем темам
    if not theme_pk:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://127.0.0.1:8000/questions/') as response:
                res = await response.json()

    # если недо получить вопрос по определенной теме
    if theme_pk:
        data = {'pk': theme_pk}
        async with aiohttp.ClientSession() as session:
            async with session.post(url='http://127.0.0.1:8000/themes/', data=data) as response:
                res = await response.json()

    # берем рандомный вопрос из тех что получили в response
    question = choice([quest for quest in res])
    return question





# получение ответов по заданному вопросу
async def get_answers(question):
    # объек который будет передан в post запросе
    data_to = question

    # передаем в запрос объект который содержит имя вопроса
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://127.0.0.1:8000/answers/', data=data_to) as response:

            answers = await response.json()

            # перемешиваем ответы
            shuffle(answers)

            # засовываем в список res name ответов
            answer_name = [answ['name'] for answ in answers]

            # красивый вывод ответов
            for indx, answ in enumerate(answer_name):
                answer_name[indx] = f'{indx + 1}. {answ}'

            answ_out = '\n'.join(answer_name)

            text = f'Вопрос:\n' \
                   f'{question["name"]}\n' \
                   f'-------------------\n' \
                   f'Ответы:\n' \
                   f'{answ_out}'
            return answers, text


