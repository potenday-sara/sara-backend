from rest_framework.routers import DefaultRouter

from answers.views import AnswerViewSet

router = DefaultRouter()
router.register("", AnswerViewSet, basename="answers")
urlpatterns = router.urls
