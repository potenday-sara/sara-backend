from django.db import models

from core.models import CommonModel
from questions.models.ai_models import AIType, LanguageType


class Question(CommonModel):
    type = models.CharField(max_length=4, choices=AIType.choices)
    language = models.CharField(max_length=4, choices=LanguageType.choices)
    content = models.TextField()
    product = models.TextField()
    hidden = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)

    class Meta:
        db_table = "questions"
        app_label = "questions"
        verbose_name = "질문"


class Comment(CommonModel):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    content = models.TextField()
    nickname = models.CharField(max_length=20)

    class Meta:
        db_table = "comments"
        app_label = "questions"
        verbose_name = "댓글"


class Like(CommonModel):
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    user = models.IntegerField(default=0, verbose_name="좋아요 누른 유저 id 확장용 컬럼")

    class Meta:
        db_table = "likes"
        app_label = "questions"
        verbose_name = "좋아요"
