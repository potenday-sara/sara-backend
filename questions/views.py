from django.db import transaction
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from questions.models import Answer, Question
from questions.serializers import QuestionSerializer


class QuestionViewSet(
    ReadOnlyModelViewSet,
    CreateModelMixin,
):
    queryset = Question.objects.select_related("answer").all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            question = serializer.save()
            Answer.objects.create(
                question=question,
                content="임시 GPT 답변",
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
