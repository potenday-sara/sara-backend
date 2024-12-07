from django.db import models

from core.models import CommonModel


class ShopType(models.TextChoices):
    COUPANG = "coupang"
    ALIEXPRESS = "aliexpress"

class LanguageType(models.TextChoices):
    KO = "KO"
    JA = "JA"
    EN = "EN"

class Category(CommonModel):
    code = models.CharField(max_length=50, unique=False)
    type = models.CharField(
        choices=ShopType.choices, max_length=50, default=ShopType.COUPANG
    )
    language = models.CharField(
        max_length=4, choices=LanguageType.choices, default=LanguageType.KO
    )
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"
        app_label = "shop"
