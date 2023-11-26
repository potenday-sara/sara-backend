from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from questions.consts import QUESTION_LIST_MAX_LENGTH
from questions.models import QuestionFeedback
from questions.tests.factories import AIFactory, QuestionFactory


class QuestionsView_테스트(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.url = "/questions/"
        cls.question_list = QuestionFactory.create_batch(50, type="sara")
        cls.ai = AIFactory(type="sara")

    def test_questions_조회_요청_성공_시(self):
        self.question_list[0].hidden = True
        self.question_list[0].save()

        response = self.client.get(self.url)

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("질문 목록이 리턴된다."):
            self.assertTrue(len(self.question_list) >= 1)
        with self.subTest("히든 처리된 질문은 제외된다."):
            self.assertNotIn(
                self.question_list[0].id, map(lambda x: x["id"], response.data)
            )
        with self.subTest("설정된 최대 개수를 넘지 않는다."):
            self.assertTrue(len(response.data) <= QUESTION_LIST_MAX_LENGTH)

    @patch("questions.views.Producer")
    def test_question_등록_요청_성공_시(self, mock_producer):
        mock_producer.return_value.produce.return_value = None
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

    def test_questions_feedback_요청_성공_시(self):
        response = self.client.post(
            self.url + f"{self.question_list[0].id}" + "/feedback/",
            data={"feedback": "1", "question": self.question_list[0].id},
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("questions feedback 데이터가 생성된다"):
            QuestionFeedback.objects.get(question=self.question_list[0], feedback="1")
