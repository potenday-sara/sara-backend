from django.db import models

from core.models import CommonModel


class Question(CommonModel):
    class QuestionType(models.TextChoices):
        SARA = "sara"
        MARA = "mara"

    type = models.CharField(max_length=4, choices=QuestionType.choices)
    content = models.TextField()
    product = models.TextField()

    class Meta:
        db_table = "questions"
        app_label = "questions"
        verbose_name = "질문"


class Answer(CommonModel):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = "answers"
        app_label = "questions"
        verbose_name = "답변"
