from collections import defaultdict
from datetime import datetime
from unittest.mock import patch

import freezegun
from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from shop.services import CoupangAPI, CoupangClient


class CoupangClient_테스트(TestCase):
    def test_인스턴스_생성_시(self):
        coupang_client = CoupangClient()
        with self.subTest("access_key가 정상적으로 설정된다."):
            self.assertEqual(coupang_client.api_key, settings.COUPANG_API_KEY)

        with self.subTest("secret_key가 정상적으로 설정된다."):
            self.assertEqual(coupang_client.api_secret, settings.COUPANG_API_SECRET)

        with self.subTest("host가 정상적으로 설정된다."):
            self.assertEqual(coupang_client.host, settings.COUPANG_API_HOST)

        with self.subTest("base_path이 정상적으로 설정된다."):
            self.assertEqual(coupang_client.base_path, settings.COUPANG_API_BASE_PATH)

    @patch("shop.services.Session")
    def test_request_함수_호출_시(self, mock_session):
        mock_session.return_value.request.return_value = (
            mock_session.return_value.request.return_value
        )
        mock_session.return_value.request.return_value.status_code = 200
        mock_session.return_value.request.return_value.json.return_value = {
            "data": "test",
        }
        coupang_client = CoupangClient()
        response = coupang_client.request("get", "/test/")

        with self.subTest("request 함수가 정상적으로 호출된다."):
            mock_session.return_value.request.assert_called_once_with(
                method="get",
                url=f"{coupang_client.host}{coupang_client.base_path}/test/",
                headers={
                    "Authorization": coupang_client._get_authorization(
                        "get",
                        f"{coupang_client.base_path}/test/",
                        None,
                    ),
                    "Content-Type": "application/json",
                },
                params=None,
                data=None,
            )

        with self.subTest("status_code가 정상적으로 리턴된다."):
            self.assertEqual(response.status_code, 200)

        with self.subTest("json이 정상적으로 리턴된다."):
            self.assertEqual(response.json(), {"data": "test"})

    def test_get_authorization_함수_호출_시(self):
        coupang_client = CoupangClient()
        authorization = coupang_client._get_authorization(
            "get",
            f"{coupang_client.base_path}/test/",
            None,
        )

        with self.subTest("authorization이 정상적으로 리턴된다."):
            self.assertIn("CEA", authorization)
            self.assertIn("access-key", authorization)
            self.assertIn("signed-date", authorization)
            self.assertIn("signature", authorization)


class CouponAPI_테스트(TestCase):
    @patch("shop.services.CoupangClient.request")
    def test_get_product_list_함수_호출_시(self, mock_request):
        coupang_data = [
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

        mock_request.return_value = mock_request.return_value
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "data": coupang_data,
        }
        coupang_api = CoupangAPI()
        response_data = coupang_api.get_product_list("test")

        with self.subTest("request 함수가 정상적으로 호출된다."):
            mock_request.assert_called_once_with(
                method="GET",
                url="/products/bestcategories/test",
                params={
                    "limit": 32,
                },
            )

        with self.subTest("json이 정상적으로 리턴된다."):
            self.assertEqual(response_data, coupang_data)

    @freezegun.freeze_time("2024-01-01")
    @patch("shop.services.CoupangClient.request")
    def test_get_report_data_함수_호출_시(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {"data": []}
        coupang_api = CoupangAPI()
        response_data = coupang_api.get_report_data()

        urls = ["clicks", "orders", "cancels", "commission"]
        start_date = datetime.now() - timezone.timedelta(days=30)
        end_date = datetime.now()
        date_range = {
            "startDate": start_date.strftime("%Y%m%d"),
            "endDate": end_date.strftime("%Y%m%d"),
        }

        except_date = defaultdict(lambda: defaultdict(int))
        for url in urls:
            current_date = start_date

            while current_date <= end_date:
                formatted_date = current_date.strftime("%Y-%m-%d")
                except_date[url][formatted_date] = 0
                current_date += timezone.timedelta(days=1)

        with self.subTest("request 함수가 정상적으로 호출된다."):
            for url in urls:
                mock_request.assert_any_call(
                    method="GET",
                    url=f"/reports/{url}",
                    params=date_range,
                )

        with self.subTest("json이 정상적으로 리턴된다."):
            self.assertEqual(len(response_data.keys()), len(except_date.keys()))

    @patch("shop.services.CoupangClient.request")
    def test_search_product_함수_호출_시(self, mock_request):
        coupang_data = [
            {
                "rank": 1,
                "isRocket": True,
                "isFreeShipping": True,
                "productId": 1,
                "productName": "테스트 상품",
                "productPrice": 10000,
                "productImage": "https://image.url",
                "productUrl": "https://product.url",
            }
        ]

        mock_request.return_value = mock_request.return_value
        mock_request.return_value.status_code = 200
        mock_request.return_value.json.return_value = {
            "data": {
                "productData": coupang_data,
            },
        }
        coupang_api = CoupangAPI()
        response_data = coupang_api.search_product("test")

        with self.subTest("request 함수가 정상적으로 호출된다."):
            mock_request.assert_called_once_with(
                method="GET",
                url="/products/search",
                params={
                    "keyword": "test",
                },
            )

        with self.subTest("json이 정상적으로 리턴된다."):
            self.assertEqual(response_data, coupang_data)
