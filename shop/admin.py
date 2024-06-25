import json

from django.contrib import admin

from core.cache import RedisCache
from shop.consts import REPORT_TTL
from shop.models import Category
from shop.services import CoupangAPI


class CategoryAdmin(admin.ModelAdmin):
    fields = ["code", "type", "name"]
    list_display = ["code", "type", "name"]
    search_fields = ["code", "type", "name"]
    list_display_links = ["code", "type", "name"]

    def changelist_view(self, request, extra_context=None):
        cache_key = "shop:report"
        cached_data = RedisCache().fetch_per_cache(
            key=cache_key,
            ttl=REPORT_TTL,
            beta=1,
            force_recompute=True,
            recompute_function=CoupangAPI().get_report_data,
        )

        # 커스텀 컨텍스트 생성
        if extra_context is None:
            extra_context = {}
        extra_context["report_data"] = json.dumps(cached_data)

        # 기본 changelist_view 메소드 호출
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Category, CategoryAdmin)
