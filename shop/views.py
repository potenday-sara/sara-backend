from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.cache import RedisCache
from shop.consts import SHOP_GOODS_LIST_TTL
from shop.models import Category
from shop.serializers import CategorySerializer, GoodsSerializer
from shop.services import CoupangAPI


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    @action(detail=True, methods=["GET"], serializer_class=GoodsSerializer)
    def goods(self, request, *args, **kwargs):
        category = self.get_object()

        cache_key = f"shop:category:goods:{category.code}"
        cached_data = RedisCache().fetch_per_cache(
            key=cache_key,
            ttl=SHOP_GOODS_LIST_TTL,
            beta=1,
            force_recompute=True,
            recompute_function=CoupangAPI().get_product_list,
            category_code=category.code,
        )

        serializer = self.get_serializer(cached_data, many=True)
        return Response(serializer.data)
