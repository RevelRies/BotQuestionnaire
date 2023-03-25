from .serializers import ThemeSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Theme, Question, Answer

class ThemeView(APIView):
    def get(self, request: Request):
        themes = Theme.objects.all()
        themes = ThemeSerializer(themes, many=True).data

        res = []
        for theme in themes:
            theme_name = theme['name']
            theme_pk = Theme.objects.get(name=theme_name).pk
            res.append({'name': theme_name, 'pk': theme_pk})

        return Response(res)

    def post(self, request: Request):
        theme_pk = request.data['pk']
        questions = Question.objects.filter(theme=theme_pk)
        return Response(ThemeSerializer(questions, many=True).data)


class QuestionView(APIView):
    def get(self, request: Request):
        questions = Question.objects.all()
        return Response(QuestionSerializer(questions, many=True).data)


class QuestionAddView(APIView):
    def post(self, request: Request):
        '''функция которая проверяет есть ли этот вопрос в БД и если такого не имеется, то добавлет его в БД
        и привязывает к нему ответы
        :param request:
        :return:
        '''
        theme_pk = request.data['theme_pk']
        rows = request.data['rows'].split('\n')

        for row in rows:

            # парсим строку на вопрос, правильный ответ и неправильные ответы
            st = list(map(lambda elem: elem.strip(), row.split(':')))

            question_name = st[0]
            right_answer = st[1]
            wrong_answers = st[2:]

            # делаем проверку - существует ли в БД уже такой вопрос
            try:
                Question.objects.get(name=question_name)
                continue
            except: pass

            # добавляем вопрос в БД и получаем его pk
            theme_object = Theme.objects.get(pk=theme_pk)
            Question.objects.create(name=question_name, theme=theme_object)
            question_pk = Question.objects.get(name=question_name).pk

            # добавляем правильный ответ
            question_object = Question.objects.get(pk=question_pk)
            Answer.objects.create(name=right_answer, question=question_object, correct=True)

            # добавляем неправильные ответы
            for answer in wrong_answers:
                Answer.objects.create(name=answer, question=question_object, correct=False)

        return Response(True)


class AnswerView(APIView):
    def get(self, request: Request):
        answers = Answer.objects.all()
        return Response(AnswerSerializer(answers, many=True).data)


    def post(self, request: Request):
        # получаем имя вопроса чтобы потом по нему найти pk этого вопроса
        question_name = request.data['name']
        question_pk = Question.objects.get(name=question_name).pk

        # с помощью полученного pk вопроса ищем связанные с ним ответы
        answers = Answer.objects.filter(question=question_pk)
        return Response(AnswerSerializer(answers, many=True).data)

