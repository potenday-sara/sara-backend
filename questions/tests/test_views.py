from django.test import TestCase
from rest_framework.test import APIClient

from questions.tests.factories import QuestionFactory


class QuestionsView(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.url = "/questions/"
        cls.question_list = QuestionFactory.create_batch(10, type="sara")

    def test_questions_조회_요청_성공_시(self):
        response = self.client.get(self.url)

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("질문 목록이 리턴된다."):
            self.assertEqual(len(response.data), len(self.question_list))
