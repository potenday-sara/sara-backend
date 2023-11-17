from django.db.models import Count, F, Window
from django.db.models.functions import Rank
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from questions.models import Question
from rank.serializers import RankSerializer


class RankViewSet(GenericViewSet, ListModelMixin):
    serializer_class = RankSerializer

    def get_queryset(self):
        serializer = self.get_serializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        ai_type = serializer.validated_data["type"]

        rank = (
            Question.objects.filter(type=ai_type)
            .values("product")
            .annotate(total=Count("id"))
            .annotate(rank=Window(expression=Rank(), order_by=F("total").desc()))
            .values("product", "rank")
            .order_by("rank")
        )
        return rank
