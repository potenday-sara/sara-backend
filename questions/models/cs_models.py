from django.db import models

from core.models import CommonModel


class QuestionFeedback(CommonModel):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    feedback = models.IntegerField(choices=[(1, "good"), (0, "normal"), (-1, "bad")])

    class Meta:
        db_table = "question_feedbacks"
        app_label = "questions"
        verbose_name = "질문 피드백"


class Feedback(CommonModel):
    question = models.ForeignKey("Question", on_delete=models.CASCADE, null=True)
    content = models.TextField()

    # 추후 유저 모델이 생기면 수정
    user = models.IntegerField(default=0)

    class Meta:
        db_table = "feedbacks"
        app_label = "questions"
        verbose_name = "피드백"
