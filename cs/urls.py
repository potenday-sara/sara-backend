from rest_framework.routers import DefaultRouter

from cs.views import FeedbackViewSet

router = DefaultRouter()
router.register("feedback", FeedbackViewSet, basename="feedback")

urlpatterns = router.urls
