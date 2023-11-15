from rest_framework.routers import DefaultRouter

from status.views import StatusViewSet

router = DefaultRouter()
router.register("", StatusViewSet, basename="status")

urlpatterns = router.urls
