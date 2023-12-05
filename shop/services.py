from django.conf import settings
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class CoupangClient:
    def __init__(self):
        self.api_key = settings.COUPANG_API_KEY
        self.api_secret = settings.COUPANG_API_SECRET
        self.headers = {
            "x-coupang-ace-api-key": self.api_key,
            "x-coupang-ace-secret-key": self.api_secret,
        }

    def request(self, method, url, params=None, data=None):
        session = Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        session.mount("https://", HTTPAdapter(max_retries=retry))
        session.mount("http://", HTTPAdapter(max_retries=retry))

        response = session.request(
            method=method, url=url, headers=self.headers, params=params, data=data
        )
        return response


class CoupangAPI:
    def __init__(self):
        self.client = CoupangClient()

    def get_product_list(self, keyword, limit=10, page=1):
        url = "https://api-gateway.coupang.com/v2/providers/affiliate_open_api/apis/openapi/products/search"

        querystring = {
            "keyword": keyword,
            "limit": limit,
            "subId": "saramara",
            "subId2": "saramara",
            "page": page,
        }

        return self.client.request(method="GET", url=url, params=querystring)
