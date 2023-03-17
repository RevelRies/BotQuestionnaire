from django.db import models


# тема
class Theme(models.Model):
    name = models.TextField(verbose_name='Название темы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


# вопрос
class Question(models.Model):
    name = models.TextField(verbose_name='вопрос')
    theme = models.ForeignKey(to='Theme', on_delete=models.CASCADE, verbose_name='тема вопроса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

# ответ на вопрос
class Answer(models.Model):
    name = models.TextField(verbose_name='ответ')
    correct = models.BooleanField(verbose_name='правильный ли ответ')
    question = models.ForeignKey(to='Question', on_delete=models.CASCADE, verbose_name='вопрос')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'