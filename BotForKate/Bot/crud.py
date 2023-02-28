import aiohttp
import asyncio
from random import choice

# получение всех тем
async def get_themes():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/themes/') as response:

            res = await response.json()
            themes = [th['name'] for th in res]
            return themes


# получение рандомного вопроса по всем темам или по определенной
# если нужна определенная темя то атрибут specific=True а в *args передается название темы
async def get_random_question(specific, *args):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://127.0.0.1:8000/questions/') as response:

            res = await response.json()

            if specific:
                pass
            else:
                question = choice([quest for quest in res])

            return question

# получение ответов по заданному вопросу
async def get_answers(question):
    # объек который будет передан в post запросе
    data_to = question

    # передаем в запрос объект который содержит имя вопроса
    async with aiohttp.ClientSession() as session:
        async with session.post(url='http://127.0.0.1:8000/answers/', data=data_to) as response:

            return await response.json()


