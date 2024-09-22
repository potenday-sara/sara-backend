import json

from django.contrib import admin
from django.db.models import Count, QuerySet
from django.db.models.functions import TruncDay
from rangefilter.filters import DateRangeFilter

from answers.models import Answer
from questions.models import AI, Comment, Feedback, Question, QuestionFeedback
from questions.serializers import QuestionDateCountSerializer


class AIAdmin(admin.ModelAdmin):
    fields = ["type", "language", "instruction"]
    list_display = [
        "type",
        "language",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["type", "language"]
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


class CommentsInline(admin.StackedInline):
    fields = ["nickname", "content", "created_at"]
    readonly_fields = ["nickname", "content", "created_at"]
    model = Comment
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fields = ["type", "language", "content", "product", "hidden"]
    ordering = ["-created_at"]
    list_display = [
        "type",
        "language",
        "content",
        "product",
        "hidden",
        "get_latest_questionfeedback",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        ("created_at", DateRangeFilter),
        ("updated_at", DateRangeFilter),
        ("language"),
        ("questionfeedback__feedback"),
    ]
    search_fields = ["content", "product"]
    list_display_links = ["content", "product"]
    readonly_fields = ["product", "content", "created_at", "updated_at"]
    inlines = [
        AnswerInline,
        CommentsInline,
        QuestionFeedbackInline,
        FeedbackInline,
    ]
    actions = ["set_question_hidden"]

    def get_latest_questionfeedback(self, obj: Question):
        feedback = obj.questionfeedback_set.all().order_by("-created_at").first()
        return feedback if feedback else None

    get_latest_questionfeedback.short_description = "피드백"

    def set_question_hidden(self, request, queryset: QuerySet[Question]):
        del request
        queryset.update(hidden=True)

    set_question_hidden.short_description = "선택된 항목을 숨기기"

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

        # 피드백이 있는 질문 수
        feedback_good_count = (
            Question.objects.filter(questionfeedback__feedback=1).distinct().count()
        )
        feedback_normal_count = (
            Question.objects.filter(questionfeedback__feedback=0).distinct().count()
        )
        feedback_bad_count = (
            Question.objects.filter(questionfeedback__feedback=-1).distinct().count()
        )
        feedback_count = (
            feedback_good_count + feedback_normal_count + feedback_bad_count
        )
        if total_count > 0:
            participation_rate = (feedback_count / total_count) * 100
        else:
            participation_rate = 0

        if feedback_count > 0:
            feedback_average = (
                5 * feedback_good_count
                + 3 * feedback_normal_count
                + 1 * feedback_bad_count
            ) / feedback_count
        else:
            feedback_average = 0

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
        extra_context["participation_rate"] = participation_rate
        extra_context["feedback_average"] = feedback_average

        # 기본 changelist_view 메소드 호출
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Question, QuestionAdmin)
