from django.db import models

class QuestionMessage(models.Model):
    message_id = models.BigIntegerField(unique=True, verbose_name='ID вопроса')
    date = models.DateTimeField(verbose_name='Дата вопроса')
    user_id = models.BigIntegerField(verbose_name='ID пользователя')
    username = models.CharField(max_length=255, null=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=255, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, verbose_name='Фамилия')
    text = models.TextField(verbose_name='Текст вопроса')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        db_table = 'questions'


class AnswerMessage(models.Model):
    message_id = models.BigIntegerField(unique=True, verbose_name='ID вопроса')
    date = models.DateTimeField(verbose_name='Дата ответа')
    user_id = models.BigIntegerField(verbose_name='ID пользователя')
    username = models.CharField(max_length=255, null=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=255, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, verbose_name='Фамилия')
    text = models.TextField(verbose_name='Текст ответа')
    question = models.ForeignKey(QuestionMessage, on_delete=models.CASCADE, related_name='answers')
    reply_to_msg_id = models.BigIntegerField(verbose_name='ID ответа на вопрос')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        db_table = 'answers'


class LastParsed(models.Model):
    last_parsed_id = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = 'Последний парсинг'
        verbose_name_plural = 'Последние парсинги'
        db_table = 'last_parsed'


class FilteredQuestion(models.Model):
    original_message_id = models.BigIntegerField(unique=True, verbose_name='ID вопроса')
    date = models.DateTimeField(verbose_name='Дата вопроса')
    user_id = models.BigIntegerField(verbose_name='ID пользователя')
    username = models.CharField(max_length=255, null=True, verbose_name='Имя пользователя')
    first_name = models.CharField(max_length=255, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=255, null=True, verbose_name='Фамилия')
    text = models.TextField(verbose_name='Текст вопроса')

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Отфильтрованный Вопрос'
        verbose_name_plural = 'Отфильтрованные Вопросы'
        db_table = 'filtered_questions'

