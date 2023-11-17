from django.db import models

from core.models import CommonModel


class Feedback(CommonModel):
    content = models.TextField()

    # 추후 유저 모델이 생기면 수정
    user = models.IntegerField(default=0)

    class Meta:
        db_table = "feedbacks"
        app_label = "cs"
        verbose_name = "피드백"
