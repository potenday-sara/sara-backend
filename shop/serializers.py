from rest_framework import serializers
from rest_framework.fields import BooleanField, CharField, IntegerField
from rest_framework.serializers import ModelSerializer

from core.serializers import RequestSerializer
from shop.models import Category, ShopType


class CategoryListRequestParamSerializer(RequestSerializer):
    language = serializers.ChoiceField(
        choices=[
            ("KO", "KO"),
            ("EN", "EN"),
            ("JA", "JA"),
        ],
        default="KO",
    )


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "code",
            "type",
            "name",
        )


class GoodsSerializer(RequestSerializer):
    is_rocket = BooleanField(source="isRocket", required=False)
    is_free_shipping = BooleanField(source="isFreeShipping", required=False)
    product_id = IntegerField(source="productId")
    product_image = CharField(source="productImage", required=False)
    product_name = CharField(source="productName")
    product_price = CharField(source="productPrice")
    product_url = CharField(source="productUrl")
    product_price_currency = CharField(source="productPriceCurrency", required=False)


class CategoryGoodsSerializer(GoodsSerializer):
    category_name = CharField(source="categoryName", required=False)


class SearchGoodsSerializer(GoodsSerializer):
    rank = IntegerField(required=False)


class SearchRequestSerializer(RequestSerializer):
    keyword = CharField(required=True)
    language = serializers.ChoiceField(
        choices=[
            ("KO", "KO"),
            ("EN", "EN"),
            ("JA", "JA"),
        ],
        default="KO",
    )
