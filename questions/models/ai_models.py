from django.db import models

from core.models import CommonModel


class AIType(models.TextChoices):
    SARA = "sara"
    MARA = "mara"

class LanguageType(models.TextChoices):
    KO = "KO"
    JA = "JA"
    EN = "EN"

class AI(CommonModel):
    type = models.CharField(max_length=4, choices=AIType.choices)
    language = models.CharField(max_length=4, choices=LanguageType.choices)
    instruction = models.TextField()

    class Meta:
        db_table = "ai"
        app_label = "questions"
        verbose_name = "AI"
