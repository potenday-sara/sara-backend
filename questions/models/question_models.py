from django.db import models

from core.models import CommonModel
from questions.models.ai_models import AIType


class Question(CommonModel):
    type = models.CharField(max_length=4, choices=AIType.choices)
    content = models.TextField()
    product = models.TextField()
    hidden = models.BooleanField(default=False)

    class Meta:
        db_table = "questions"
        app_label = "questions"
        verbose_name = "질문"


class QuestionFeedback(CommonModel):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    feedback = models.IntegerField(choices=[(1, "good"), (0, "normal"), (-1, "bad")])

    class Meta:
        db_table = "question_feedbacks"
        app_label = "questions"
        verbose_name = "질문 피드백"
