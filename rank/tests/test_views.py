from django.test import TestCase
from rest_framework.test import APIClient

from questions.models import QuestionFeedback
from questions.tests.factories import QuestionFactory


class RankView_테스트(TestCase):
    client_class = APIClient

    @classmethod
    def setUpTestData(cls):
        cls.url = "/rank/"
        cls.product_list = {"product1": 5, "product2": 3, "product3": 1}
        for product, product_amount in cls.product_list.items():
            QuestionFactory.create_batch(
                product_amount,
                type="sara",
                product=product,
            )

    def test_questions_조회_요청_성공_시(self):
        response = self.client.get(
            self.url,
            data={"type": "sara"},
        )

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)
        with self.subTest("랭킹 목록이 리턴된다."):
            self.assertEqual(len(response.data), len(self.product_list))
            product_rank = [rank["product"] for rank in response.data]
            self.assertEqual(product_rank, list(self.product_list.keys()))
