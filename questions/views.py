from django.db import transaction
from django.db.models import F
from django.db.models.functions import Random
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from questions.consts import QUESTION_LIST_MAX_LENGTH
from questions.models import Like, Question, QuestionFeedback
from questions.serializers import (
    CommentSerializer,
    FeedbackSerializer,
    QuestionFeedbackSerializer,
    QuestionListRequestParamsSerializer,
    QuestionSerializer,
)
from questions.tasks import task_get_answer


class QuestionViewSet(
    ReadOnlyModelViewSet,
    CreateModelMixin,
):
    class QuestionLimitOffsetPagination(LimitOffsetPagination):
        default_limit = 30

    queryset = (
        Question.objects.select_related("answer")
        .prefetch_related("comment_set", "like_set")
        .all()
    )
    serializer_class = QuestionSerializer
    pagination_class = QuestionLimitOffsetPagination

    @swagger_auto_schema(query_serializer=QuestionListRequestParamsSerializer)
    def list(self, request, *args, **kwargs):
        request_serializer = QuestionListRequestParamsSerializer(
            data=request.query_params
        )
        request_serializer.is_valid(raise_exception=True)

        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.filter(
            hidden=False,
            answer__checked=True,
        )
        if request_serializer.validated_data["type"] != "all":
            queryset = queryset.filter(type=request_serializer.validated_data["type"])

        if request_serializer.validated_data["order"] == "like":
            queryset = queryset.order_by("-like_count")
        else:
            queryset = queryset.order_by("-created_at")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["get"],
    )
    def random(self, request, *args, **kwargs):
        self.pagination_class = None
        queryset = self.filter_queryset(self.get_queryset())

        queryset = (
            queryset.filter(
                hidden=False,
                answer__checked=True,
            )
            .annotate(random=Random())
            .order_by("random")[:QUESTION_LIST_MAX_LENGTH]
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            question = serializer.save()
            task_get_answer.apply_async(args=[str(question.id), serializer.data])

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

    @action(detail=True, methods=["post"], serializer_class=FeedbackSerializer)
    def cs(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question)
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CommentSerializer,
        url_path="comments",
    )
    def comments(self, request, *args, **kwargs):
        question = self.get_object()
        comments = question.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @comments.mapping.post
    def add_comment(self, request, *args, **kwargs):
        question = self.get_object()
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save(question=question)
            question.comment_count = F("comment_count") + 1
            question.save(update_fields=["comment_count"])
        return Response(status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["post"],
        url_path="like",
        serializer_class=Serializer,
    )
    def like(self, request, *args, **kwargs):
        question = self.get_object()
        with transaction.atomic():
            question.like_count = F("like_count") + 1
            question.save(update_fields=["like_count"])
            Like.objects.create(question=question)

            return Response(status=status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self, request, *args, **kwargs):
        question = self.get_object()
        with transaction.atomic():
            question.like_count = F("like_count") - 1
            question.save(update_fields=["like_count"])
            if like := Like.objects.filter(question=question).last():
                like.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
