from django.test import TestCase
from rest_framework.test import APIClient

from cs.models import Feedback


class FeedbackView_테스트(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.url = "/cs/feedback/"

    def test_feedback_요청_성공_시(self):
        response = self.client.post(
            self.url,
            data={"content": "test"},
        )
        with self.subTest("status code 201이 리턴된다."):
            self.assertEqual(response.status_code, 201)
        with self.subTest("feedback 데이터가 생성된다"):
            self.assertEqual(Feedback.objects.count(), 1)
