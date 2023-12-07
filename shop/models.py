from django.db import models

from core.models import CommonModel


class Category(CommonModel):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = "category"
        app_label = "shop"
