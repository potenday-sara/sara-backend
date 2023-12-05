from rest_framework.response import Response
from rest_framework.views import APIView

from shop.services import CoupangAPI


class GoodsViewSet(APIView):
    def get(self, request):
        serializer = GoodsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        goods = serializer["goods"]

        shop_data = CoupangAPI().get_product_list(goods)
        return Response(shop_data)
