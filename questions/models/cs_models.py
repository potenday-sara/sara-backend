from django.db import models

from core.models import CommonModel


class QuestionFeedback(CommonModel):
    class FeedbackType(models.IntegerChoices):
        GOOD = 1, "good"
        NORMAL = 0, "normal"
        BAD = -1, "bad"

    question = models.OneToOneField("Question", on_delete=models.CASCADE)
    feedback = models.IntegerField(choices=FeedbackType.choices)

    class Meta:
        db_table = "question_feedbacks"
        app_label = "questions"
        verbose_name = "질문 피드백"

    def __str__(self):
        return self.FeedbackType(self.feedback).label


class Feedback(CommonModel):
    question = models.OneToOneField("Question", on_delete=models.CASCADE, null=True)
    content = models.TextField()

    # 추후 유저 모델이 생기면 수정
    user = models.IntegerField(default=0)

    class Meta:
        db_table = "feedbacks"
        app_label = "questions"
        verbose_name = "피드백"
