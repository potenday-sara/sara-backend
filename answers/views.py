from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from answers.models import Answer
from answers.serializers import AnswerSerializer


class AnswerViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Answer.objects.select_related("question").all()
    serializer_class = AnswerSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.checked:
            instance.checked = True
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
