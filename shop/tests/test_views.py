from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from shop.models import Category
from shop.tests.factories import CategoryFactory


class CategoryView_목록_요청_테스트(TestCase):
    client_class: APIClient = APIClient
    url: str
    category_list: list[Category]

    @classmethod
    def setUpTestData(cls):
        cls.url = "/shop/categories/"
        cls.category_list = CategoryFactory.create_batch(10)

    def test_categories_조회_요청_성공_시(self):
        response = self.client.get(self.url)

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)

        with self.subTest("카테고리 목록이 리턴된다."):
            self.assertEqual(len(response.data), len(self.category_list))


class CategoryView_상세_요청_테스트(TestCase):
    client_class = APIClient
    url: str
    category: Category

    @classmethod
    def setUpTestData(cls):
        cls.url = "/shop/categories/"
        cls.category = CategoryFactory()

    def test_detail_category_조회_요청_성공_시(self):
        response = self.client.get(f"{self.url}{self.category.id}/")

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)

        with self.subTest("카테고리 정보가 리턴된다."):
            self.assertEqual(response.data["id"], str(self.category.id))

    def test_detail_category_없는_ID_조회_요청_시(self):
        with self.subTest("status code 404이 리턴된다."):
            response = self.client.get(f"{self.url}{0}/")
            self.assertEqual(response.status_code, 404)


class Goods_목록_요청_테스트(TestCase):
    client_class = APIClient
    url: str
    category: Category

    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryFactory()
        cls.url = f"/shop/categories/{cls.category.id}/goods/"

    @patch("shop.views.RedisCache.fetch_per_cache")
    def test_goods_조회_요청_성공_시(self, mock_fetch_per_cache):
        mock_fetch_per_cache.return_value = [
            {
                "categoryName": "테스트 카테고리",
                "isRocket": True,
                "isFreeShipping": True,
                "productId": 1,
                "productName": "테스트 상품",
                "productPrice": 10000,
                "productImage": "https://image.url",
                "productUrl": "https://product.url",
            }
        ]
        response = self.client.get(self.url)

        with self.subTest("status code 200이 리턴된다."):
            self.assertEqual(response.status_code, 200)

        with self.subTest("상품 목록이 리턴된다."):
            self.assertTrue(len(response.data) >= 1)
