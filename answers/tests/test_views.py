from django.test import TestCase
from rest_framework.test import APIClient

from answers.tests.factories import AnswerFactory


class AnswerView_테스트(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.answer = AnswerFactory()
        cls.url = f"/answers/{cls.answer.id}/"

    def test_answers_조회_요청_성공_시(self):
        response = self.client.get(self.url)

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)

        with self.subTest("답변이 리턴된다."):
            self.assertEqual(response.data["id"], str(self.answer.id))

        with self.subTest("답변의 cheked가 True로 처리된다"):
            self.assertFalse(self.answer.checked)
            self.answer.refresh_from_db()
            self.assertTrue(self.answer.checked)
