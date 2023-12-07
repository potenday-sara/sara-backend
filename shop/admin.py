from django.contrib import admin

from shop.models import Category


class CategoryAdmin(admin.ModelAdmin):
    fields = ["code", "name"]
    list_display = ["code", "name"]
    search_fields = ["code", "name"]
    list_display_links = ["code", "name"]


admin.site.register(Category, CategoryAdmin)
