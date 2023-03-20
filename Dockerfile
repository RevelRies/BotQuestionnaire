FROM python:3.10

WORKDIR /app
COPY . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

#CMD ["python", "./Bot/bot.py"]
CMD ["manage.py", "runserver"]