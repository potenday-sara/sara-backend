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

    def test_changelist_view(self):
        qa = CategoryAdmin(Category, self.site)

        request_factory = RequestFactory()
        request = request_factory.get("/admin/shop/category/")
        request.user = MockSuperUser()

        response = qa.changelist_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("report_data", response.context_data)
