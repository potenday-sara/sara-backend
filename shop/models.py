from django.db import models

from core.models import CommonModel


class ShopType(models.TextChoices):
    COUPANG = "coupang"
    ALIEXPRESS = "aliexpress"


class Category(CommonModel):
    code = models.CharField(max_length=10, unique=True)
    type = models.CharField(
        choices=ShopType.choices, max_length=30, default=ShopType.COUPANG
    )
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "category"
        app_label = "shop"
