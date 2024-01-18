import hashlib
import hmac
from datetime import datetime
from time import gmtime, strftime
from urllib.parse import urlencode

from django.conf import settings
from django.utils import timezone
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class CoupangClient:
    def __init__(self):
        self.api_key = settings.COUPANG_API_KEY
        self.api_secret = settings.COUPANG_API_SECRET
        self.host = settings.COUPANG_API_HOST
        self.base_path = settings.COUPANG_API_BASE_PATH

    def request(self, method, url, params=None, data=None):
        session = Session()
        retry = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        session.mount("https://", HTTPAdapter(max_retries=retry))

        headers = {
            "Authorization": self._get_authorization(
                method,
                f"{self.base_path}{url}",
                urlencode(params) if params else None,
            ),
            "Content-Type": "application/json",
        }

        response = session.request(
            method=method,
            url=f"{self.host}{self.base_path}{url}",
            headers=headers,
            params=params,
            data=data,
        )
        return response

    def _get_authorization(self, method, url, query=None):
        datetime_gmt = (
            strftime("%y%m%d", gmtime()) + "T" + strftime("%H%M%S", gmtime()) + "Z"
        )
        message = datetime_gmt + method + url + (query if query else "")

        signature = hmac.new(
            bytes(self.api_secret, "utf-8"), message.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        return f"CEA algorithm=HmacSHA256, access-key={self.api_key}, signed-date={datetime_gmt}, signature={signature}"


class CoupangAPI:
    def __init__(self):
        self.client = CoupangClient()

    def get_product_list(self, category_code, limit=32):
        url = f"/products/bestcategories/{category_code}"

        querystring = {
            "limit": limit,
        }

        response_data = self.client.request(
            method="GET",
            url=url,
            params=querystring,
        ).json()

        return response_data["data"]

    def get_report_data(self):
        urls = [
            "clicks",
            "orders",
            "cancels",
            "commission",
        ]
        start_date: datetime = timezone.now() - timezone.timedelta(days=30)
        end_date: datetime = timezone.now()

        querystring = {
            "startDate": start_date.strftime("%Y%m%d"),
            "endDate": end_date.strftime("%Y%m%d"),
        }

        response_data = {
            url: self.client.request(
                method="GET",
                url=f"/reports/{url}",
                params=querystring,
            )
            .json()
            .get("data")
            for url in urls
        }

        return response_data

    def search_product(self, keyword: str):
        url = f"/products/search"

        querystring = {
            "keyword": keyword,
        }

        response_data = self.client.request(
            method="GET",
            url=url,
            params=querystring,
        ).json()

        return response_data["data"]["productData"]
