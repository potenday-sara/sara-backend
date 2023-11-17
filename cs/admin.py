from django.contrib import admin

from cs.models import Feedback


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
