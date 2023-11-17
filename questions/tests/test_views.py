from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from questions.models import QuestionFeedback
from questions.tests.factories import AIFactory, QuestionFactory


class QuestionsView_테스트(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.url = "/questions/"
        cls.question_list = QuestionFactory.create_batch(10, type="sara")
        cls.ai = AIFactory(type="sara")

    def test_questions_조회_요청_성공_시(self):
        response = self.client.get(self.url)

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("질문 목록이 리턴된다."):
            self.assertEqual(len(response.data), len(self.question_list))

    @patch("questions.views.GPTService.get_answer")
    def test_question_등록_요청_성공_시(self, mock_get_answer):
        mock_get_answer.return_value = "테스트 답변"
        data = {
            "type": "sara",
            "product": "테스트 상품",
            "content": "테스트 질문",
        }
        response = self.client.post(self.url, data=data)

        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("질문이 생성된다."):
            self.assertEqual(response.data["product"], data["product"])
            self.assertEqual(response.data["content"], data["content"])
            self.assertEqual(response.data["type"], data["type"])
            self.assertEqual(response.data["answer"], "테스트 답변")

    def test_questions_feedback_요청_성공_시(self):
        response = self.client.post(
            self.url + f"{self.question_list[0].id}" + "/feedback/",
            data={"feedback": "1", "question": self.question_list[0].id},
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("questions feedback 데이터가 생성된다"):
            QuestionFeedback.objects.get(question=self.question_list[0], feedback="1")
