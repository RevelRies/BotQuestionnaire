FROM python:3.10

WORKDIR /app
COPY . /app
COPY ./Bot /app


RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["manage.py", "runserver"]

CMD ["python", "bot.py"]