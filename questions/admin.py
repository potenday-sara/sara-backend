from django.contrib import admin

from questions.models import Answer, Question, QuestionFeedback


class AnswerInline(admin.StackedInline):
    fields = ["content"]
    model = Answer
    extra = 1


class QuestionFeedbackInline(admin.StackedInline):
    fields = ["feedback"]
    model = QuestionFeedback
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fields = ["type", "content", "product"]
    list_display = [
        "type",
        "content",
        "product",
        "created_at",
        "updated_at",
    ]
    search_fields = ["content", "product"]
    list_display_links = ["content", "product"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [AnswerInline, QuestionFeedbackInline]


admin.site.register(Question, QuestionAdmin)
