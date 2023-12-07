from rest_framework.routers import DefaultRouter

from shop.views import CategoryViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="shop_category")

urlpatterns = router.urls
