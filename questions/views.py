from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from event_services.producer import Producer
from questions.models import Question, QuestionFeedback
from questions.serializers import QuestionFeedbackSerializer, QuestionSerializer


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
            producer = Producer()
            producer.produce(
                topic="question", key=str(question.id), value=dict(serializer.data)
            )

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["post"], serializer_class=QuestionFeedbackSerializer)
    def feedback(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        QuestionFeedback.objects.create(
            question=question,
            feedback=serializer.validated_data["feedback"],
        )
        return Response(status=status.HTTP_201_CREATED)
