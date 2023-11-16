from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from cs.models import Feedback
from cs.serializers import FeedbackSerializer


class FeedbackViewSet(GenericViewSet, CreateModelMixin):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
