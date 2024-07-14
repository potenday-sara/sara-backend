from django.db import models

from core.models import CommonModel


class ShopType(models.TextChoices):
    COUPANG = "coupang"
    ALIEXPRESS = "aliexpress"


class Category(CommonModel):
    code = models.CharField(max_length=50, unique=True)
    type = models.CharField(
        choices=ShopType.choices, max_length=50, default=ShopType.COUPANG
    )
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "category"
        app_label = "shop"
