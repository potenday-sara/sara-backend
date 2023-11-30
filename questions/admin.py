from django.contrib import admin

from answers.models import Answer
from questions.models import AI, Feedback, Question, QuestionFeedback


class AnswerInline(admin.StackedInline):
    fields = ["content"]
    model = Answer
    extra = 1


class QuestionFeedbackInline(admin.StackedInline):
    fields = ["feedback"]
    model = QuestionFeedback
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
    readonly_fields = ["created_at", "updated_at"]
    inlines = [AnswerInline, QuestionFeedbackInline]


admin.site.register(Question, QuestionAdmin)


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
    fields = ["content"]
    list_display = [
        "content",
        "created_at",
        "updated_at",
    ]
    search_fields = ["content"]
    list_display_links = ["content"]
    readonly_fields = ["created_at", "updated_at"]


admin.site.register(Feedback, FeedbackAdmin)
