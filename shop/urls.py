from rest_framework.routers import DefaultRouter

from shop.views import CategoryViewSet, SearchAPIView

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="shop_category")
router.register("search", SearchAPIView, basename="shop_search")

urlpatterns = router.urls
