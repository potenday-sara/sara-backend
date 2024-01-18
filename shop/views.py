from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from core.cache import RedisCache
from shop.consts import SHOP_GOODS_LIST_TTL, SHOP_MAX_SEARCH_COUNT, SHOP_MAX_SEARCH_TTL
from shop.models import Category
from shop.serializers import (
    CategoryGoodsSerializer,
    CategorySerializer,
    SearchGoodsSerializer,
    SearchRequestSerializer,
)
from shop.services import CoupangAPI


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    @action(detail=True, methods=["GET"], serializer_class=CategoryGoodsSerializer)
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


class SearchAPIView(GenericViewSet, ListModelMixin):
    serializer_class = SearchGoodsSerializer
    pagination_class = None
    queryset = None

    def get_queryset(self):
        pass  # pragma: no cover

    @swagger_auto_schema(query_serializer=SearchRequestSerializer)
    def list(self, request, *args, **kwargs):
        cache_key = "shop:search"
        lock_count = RedisCache().redis_client.get(cache_key)

        if lock_count is None:
            RedisCache().redis_client.set(cache_key, 0, SHOP_MAX_SEARCH_TTL)
            lock_count = 0

        if int(lock_count) >= SHOP_MAX_SEARCH_COUNT:
            return Response(status=HTTP_429_TOO_MANY_REQUESTS)

        request_serializer = SearchRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)

        RedisCache().redis_client.incr(cache_key)
        search_data = CoupangAPI().search_product(
            keyword=request_serializer.validated_data.get("keyword")
        )
        serializer = self.get_serializer(search_data, many=True)
        return Response(serializer.data)
