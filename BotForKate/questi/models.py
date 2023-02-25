from django.db import models


# тема
class Theme(models.Model):
    name = models.TextField()


# вопрос
class Question(models.Model):
    name = models.TextField()
    theme = models.ForeignKey(to='Theme', on_delete=models.CASCADE)


# ответ на вопрос
class Answer(models.Model):
    name = models.TextField()
    correct = models.BooleanField()
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE)