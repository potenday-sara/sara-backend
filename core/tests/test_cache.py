import pickle
from unittest.mock import MagicMock, patch

from django.conf import settings
from django.test import TestCase

from core.cache import PERData, RedisCache


class RedisCache_테스트(TestCase):
    @patch("core.cache.Redis")
    def test_인스턴스_생성_시(self, mock_redis: MagicMock):
        RedisCache()

        with self.subTest("redis_client가 정상적으로 설정된다."):
            mock_redis.assert_called_with(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=False,
                socket_timeout=3,
                socket_connect_timeout=1,
            )

    @patch("core.cache.Redis")
    def test_get_remain_ttl_함수_호출_시(self, mock_redis: MagicMock):
        mock_redis.return_value.pttl.return_value = 1000
        redis_cache = RedisCache()
        redis_cache._get_remain_ttl("test")

        with self.subTest("redis_client.pttl 함수가 정상적으로 호출된다."):
            mock_redis.return_value.pttl.assert_called_with("test")

    @patch("core.cache.Redis")
    def test_get_cache_함수_호출_시(self, mock_redis: MagicMock):
        mock_redis.return_value.get.return_value = "test"
        redis_cache = RedisCache()
        redis_cache._get_cache("test")

        with self.subTest("redis_client.get 함수가 정상적으로 호출된다."):
            mock_redis.return_value.get.assert_called_with("test")

    @patch("core.cache.Redis")
    def test_set_cache_함수_호출_시(self, mock_redis: MagicMock):
        redis_cache = RedisCache()
        redis_cache._set_cache("test", "test", 1000)

        with self.subTest("redis_client.set 함수가 정상적으로 호출된다."):
            mock_redis.return_value.set.assert_called_with("test", "test", 1000)


class PERAlgorithmMixin_테스트(TestCase):
    @patch("core.cache.RedisCache._get_cache")
    @patch("core.cache.RedisCache._set_cache")
    def test_fetch_per_cache_함수_호출_시(
        self,
        mock_set_cache: MagicMock,
        mock_get_cache: MagicMock,
    ):
        mock_get_cache.return_value = None

        def mock_recompute_function():
            return "test"

        redis_cache = RedisCache()
        redis_cache.fetch_per_cache(
            key="test",
            ttl=1000,
            recompute_function=mock_recompute_function,
        )

        with self.subTest("_get_cache 함수가 정상적으로 호출된다."):
            mock_get_cache.assert_called_with("test")

        with self.subTest("_set_per_data 함수가 정상적으로 호출된다."):
            mock_set_cache.assert_called()

    @patch("core.cache.RedisCache._get_cache")
    @patch("core.cache.PERAlgorithmMixin._set_per_data")
    def test_fetch_per_cache_함수_호출_시_캐시_있을_경우(
        self,
        mock_set_per_data: MagicMock,
        mock_get_cache: MagicMock,
    ):
        mock_get_cache.return_value = pickle.dumps(
            PERData(
                data="test",
                computation_time=-1000,
            )
        )
        redis_cache = RedisCache()
        redis_cache.fetch_per_cache(
            key="test",
            ttl=1000,
            recompute_function=lambda: "test",
        )

        with self.subTest("_get_cache 함수가 정상적으로 호출된다."):
            mock_get_cache.assert_called_with("test")

        with self.subTest("_set_per_data 함수가 호출되지 않는다."):
            mock_set_per_data.assert_not_called()

    @patch("core.cache.RedisCache._get_cache")
    @patch("core.cache.RedisCache._set_cache")
    def test_fetch_per_cache_함수_호출_시_캐시_있을_경우_force_recompute_True_일_경우(
        self,
        mock_set_cache: MagicMock,
        mock_get_cache: MagicMock,
    ):
        mock_get_cache.return_value = pickle.dumps(
            PERData(
                data="test",
                computation_time=-1000,
            )
        )

        def mock_recompute_function():
            return "test"

        redis_cache = RedisCache()
        redis_cache.fetch_per_cache(
            key="test",
            ttl=1000,
            recompute_function=mock_recompute_function,
            force_recompute=True,
        )

        with self.subTest("PERAlgorithmMixin._get_cache 함수가 호출된다."):
            mock_get_cache.assert_called_with("test")

        with self.subTest("PERAlgorithmMixin._set_per_data 함수가 호출된다."):
            mock_set_cache.assert_called()
