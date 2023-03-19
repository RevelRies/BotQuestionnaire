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

