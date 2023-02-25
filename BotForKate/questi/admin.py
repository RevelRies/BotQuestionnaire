from django.contrib import admin
from .models import Theme, Question, Answer
from .forms import ThemeForm, QuestionForm, AnswerForm

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    form = ThemeForm


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'theme')
    form = QuestionForm


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'correct', 'question')
    form = AnswerForm