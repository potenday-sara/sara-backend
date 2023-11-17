from rest_framework.routers import DefaultRouter

from questions.views import QuestionViewSet
from rank.views import RankViewSet

router = DefaultRouter()
router.register("", RankViewSet, basename="rank")

urlpatterns = router.urls
