import math
import pickle
import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Callable

from django.conf import settings
from redis import Redis


@dataclass
class PERData:
    data: Any
    computation_time: int


class PERAlgorithmMixin(ABC):
    @staticmethod
    def _get_score(computation_time: float, beta: float) -> float:
        return computation_time * beta * -math.log(random.random() or 1)

    def _set_per_data(self, key: str, ttl: int, recompute_function: Callable, **kwargs):
        start_time = time.perf_counter()
        result_from_db = (
            recompute_function(**kwargs) if kwargs else recompute_function()
        )
        processed_time = time.perf_counter() - start_time

        self._set_cache(
            key=key,
            data=pickle.dumps(
                PERData(
                    data=result_from_db,
                    computation_time=int(processed_time * 1000),
                )
            ),
            ttl=ttl,
        )

        return result_from_db

    def fetch_per_cache(
        self,
        key: str,
        ttl: int,
        recompute_function: Callable,
        beta: float = 1,
        force_recompute: bool = False,
        **kwargs,
    ):
        cached_data = self._get_cache(key)
        if cached_data is None:
            return self._set_per_data(
                key=key,
                ttl=ttl,
                recompute_function=recompute_function,
                **kwargs,
            )

        per_data: PERData = pickle.loads(cached_data)
        expiry_ttl = self._get_remain_ttl(key)
        adjusted_computation_time = ttl * 1000 * 0.1

        if force_recompute and adjusted_computation_time > expiry_ttl:
            computation_time = adjusted_computation_time
        else:
            computation_time = per_data.computation_time

        if self._get_score(computation_time, beta) >= expiry_ttl:
            return self._set_per_data(
                key=key,
                ttl=ttl,
                recompute_function=recompute_function,
                **kwargs,
            )

        return per_data.data

    @abstractmethod
    def _get_remain_ttl(self, key: str) -> float:
        pass

    @abstractmethod
    def _get_cache(self, key: str):
        pass

    @abstractmethod
    def _set_cache(self, key: str, data, ttl: int):
        pass


class RedisCache(PERAlgorithmMixin):
    def __init__(self, decode_responses=False):
        self.redis_client: Redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=decode_responses,
            socket_timeout=3,
            socket_connect_timeout=1,
        )

    def _get_remain_ttl(self, key: str) -> float:
        return self.redis_client.pttl(key)

    def _get_cache(self, key: str):
        return self.redis_client.get(key)

    def _set_cache(self, key: str, data, ttl: int):
        self.redis_client.set(key, data, ttl)
