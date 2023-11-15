from rest_framework.routers import DefaultRouter

from questions.views import QuestionViewSet

router = DefaultRouter()
router.register("", QuestionViewSet, basename="questions")

urlpatterns = router.urls
