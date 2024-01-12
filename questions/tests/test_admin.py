from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from answers.tests.factories import AnswerFactory
from questions.admin import QuestionAdmin
from questions.models import Question
from questions.tests.factories import QuestionFactory


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
        self.assertIn("datewise_sara_counts", response.context_data)
        self.assertIn("datewise_mara_counts", response.context_data)
        self.assertIn("type_counts", response.context_data)
        self.assertIn("total_count", response.context_data)

    def test_get_latest_questionfeedback(self):
        qa = QuestionAdmin(Question, self.site)

        question = QuestionFactory(type="sara")
        AnswerFactory(question=question, checked=True)

        question_feedback = question.questionfeedback_set.create(
            feedback=1,
        )

        self.assertEqual(qa.get_latest_questionfeedback(question), question_feedback)
        self.assertIsNone(qa.get_latest_questionfeedback(Question()))

    def test_set_question_hidden(self):
        qa = QuestionAdmin(Question, self.site)

        question = QuestionFactory(hidden=False)
        question2 = QuestionFactory(hidden=False)

        qa.set_question_hidden(None, Question.objects.all())

        question.refresh_from_db()
        question2.refresh_from_db()

        self.assertTrue(question.hidden)
        self.assertTrue(question2.hidden)
