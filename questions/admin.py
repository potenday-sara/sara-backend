from django.contrib import admin

from answers.models import Answer
from questions.models import AI, Feedback, Question, QuestionFeedback


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


admin.site.register(Question, QuestionAdmin)
