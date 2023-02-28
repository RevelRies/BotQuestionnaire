from django.contrib import admin
from django.urls import path
from questi.views import ThemeView, QuestionView, AnswerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('themes/', ThemeView.as_view()),
    path('questions/', QuestionView.as_view()),
    path('answers/', AnswerView.as_view())
]
