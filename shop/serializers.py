from rest_framework.fields import BooleanField, CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from shop.models import Category


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "code",
            "name",
        )


class GoodsSerializer(Serializer):
    category_name = CharField(source="categoryName")
    is_rocket = BooleanField(source="isRocket")
    is_free_shipping = BooleanField(source="isFreeShipping")
    product_id = IntegerField(source="productId")
    product_image = CharField(source="productImage")
    product_name = CharField(source="productName")
    product_price = IntegerField(source="productPrice")
    product_url = CharField(source="productUrl")

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
