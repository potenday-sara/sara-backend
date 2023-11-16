from django.test import TestCase
from rest_framework.test import APIClient

from questions.models import QuestionFeedback
from questions.tests.factories import QuestionFactory


class QuestionsView_테스트(TestCase):
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

    def test_questions_feedback_요청_성공_시(self):
        response = self.client.post(
            self.url + f"{self.question_list[0].id}" + "/feedback/",
            data={"feedback": "1", "question": self.question_list[0].id},
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("questions feedback 데이터가 생성된다"):
            QuestionFeedback.objects.get(question=self.question_list[0], feedback="1")
