from django.contrib import admin

from shop.models import Category


class CategoryAdmin(admin.ModelAdmin):
    fields = ["id", "code", "name"]
    list_display = ["id", "code", "name"]
    search_fields = ["code", "name"]
    list_display_links = ["code", "name"]
    readonly_fields = ["id"]


admin.site.register(Category, CategoryAdmin)
