from django import forms
from .models import Theme, Question, Answer
class ThemeForm(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ('name',)
        widgets = {
            'name': forms.TextInput()
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('name', 'theme')



class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('name', 'correct', 'question')