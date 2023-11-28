from django.db import models

from core.models import CommonModel


class Answer(CommonModel):
    question = models.OneToOneField("Question", on_delete=models.CASCADE)
    content = models.TextField()
    checked = models.BooleanField(default=False)

    class Meta:
        db_table = "answers"
        app_label = "questions"
        verbose_name = "답변"
