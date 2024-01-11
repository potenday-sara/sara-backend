import json

from django.contrib import admin
from django.db.models import Count
from django.db.models.functions import TruncDay

from answers.models import Answer
from questions.models import AI, Feedback, Question, QuestionFeedback
from questions.serializers import QuestionDateCountSerializer


class AIAdmin(admin.ModelAdmin):
    fields = ["type", "instruction"]
    list_display = [
        "type",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["type"]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(AI, AIAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    fields = ["question", "content"]
    list_display = [
        "content",
        "created_at",
        "updated_at",
    ]
    search_fields = ["content"]
    list_display_links = ["content"]
    readonly_fields = ["question", "content", "created_at", "updated_at"]


admin.site.register(Feedback, FeedbackAdmin)


class AnswerInline(admin.StackedInline):
    fields = ["content"]
    readonly_fields = ["content"]
    model = Answer
    extra = 1


class QuestionFeedbackInline(admin.StackedInline):
    fields = ["feedback"]
    readonly_fields = ["feedback"]
    model = QuestionFeedback
    extra = 1


class FeedbackInline(admin.StackedInline):
    fields = ["content"]
    readonly_fields = ["content"]
    model = Feedback
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fields = ["type", "content", "product", "hidden"]
    ordering = ["-created_at"]
    list_display = [
        "type",
        "content",
        "product",
        "hidden",
        "created_at",
        "updated_at",
    ]
    search_fields = ["content", "product"]
    list_display_links = ["content", "product"]
    readonly_fields = ["product", "content", "created_at", "updated_at"]
    inlines = [
        AnswerInline,
        QuestionFeedbackInline,
        FeedbackInline,
    ]

    def changelist_view(self, request, extra_context=None):
        # 날짜별 질문 카운트
        datewise_counts = (
            Question.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )
        datewise_sara_counts = (
            Question.objects.filter(type="sara")
            .annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )
        datewise_mara_counts = (
            Question.objects.filter(type="mara")
            .annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(count=Count("id"))
            .order_by("date")
        )

        # 타입별 카운트
        type_counts = Question.objects.values("type").annotate(count=Count("id"))

        # 총 카운트
        total_count = Question.objects.count()

        # 커스텀 컨텍스트 생성
        if extra_context is None:
            extra_context = {}
        extra_context["datewise_counts"] = json.dumps(
            QuestionDateCountSerializer(
                datewise_counts,
                many=True,
            ).data
        )
        extra_context["datewise_sara_counts"] = json.dumps(
            QuestionDateCountSerializer(
                datewise_sara_counts,
                many=True,
            ).data
        )
        extra_context["datewise_mara_counts"] = json.dumps(
            QuestionDateCountSerializer(
                datewise_mara_counts,
                many=True,
            ).data
        )
        extra_context["type_counts"] = type_counts
        extra_context["total_count"] = total_count

        # 기본 changelist_view 메소드 호출
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Question, QuestionAdmin)
