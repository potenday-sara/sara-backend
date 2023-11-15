from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from status.tests.mock import MockCursor


class health_check_요청_시(TestCase):
    client_class = APIClient

    def test_요청_성공_시_status_code_200_을_리턴한다(self):
        response = self.client.get("/status/health/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class stand_by_check_요청_시(TestCase):
    client_class = APIClient

    def test_요청_성공_시_status_code_200_을_리턴한다(self):
        response = self.client.get("/status/stand-by/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    @patch("status.views.connections")
    def test_db_연결_실패_시_status_code_500_을_리턴한다(self, mock_connections):
        mock_db_alias = "mock_db"
        mock_connections.databases.keys.return_value = [mock_db_alias]
        mock_connections.getitem(mock_db_alias).cursor.return_value = MockCursor()

        response = self.client.get("/status/stand-by/")
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
