from unittest.mock import MagicMock, patch

import freezegun
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from shop.admin import CategoryAdmin
from shop.models import Category


class MockSuperUser:
    is_active = True
    is_staff = True

    def has_perm(self, perm):
        del perm
        return True


class CategoryAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    @freezegun.freeze_time("2024-01-01")
    @patch("shop.services.CoupangClient.request")
    @patch("core.cache.Redis")
    def test_changelist_view(self, mock_redis: MagicMock, mock_request: MagicMock):
        mock_redis.return_value.get.return_value = None

        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"data": []}

        qa = CategoryAdmin(Category, self.site)

        request_factory = RequestFactory()
        request = request_factory.get("/admin/shop/category/")
        request.user = MockSuperUser()

        response = qa.changelist_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("report_data", response.context_data)
