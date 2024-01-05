from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from questions.admin import QuestionAdmin
from questions.models import Question


class MockSuperUser:
    is_active = True
    is_staff = True

    def has_perm(self, perm):
        del perm
        return True


class QuestionAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_changelist_view(self):
        qa = QuestionAdmin(Question, self.site)

        request_factory = RequestFactory()
        request = request_factory.get("/admin/questions/question/")
        request.user = MockSuperUser()

        response = qa.changelist_view(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("datewise_counts", response.context_data)
        self.assertIn("type_counts", response.context_data)
        self.assertIn("total_count", response.context_data)
