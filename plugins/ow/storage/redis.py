import abc

from typing import List

import redis
from bot.utils import import_string
from plugins.ow.storage.settings import ENVIRONMENT, REDIS_CLASS


class Storage(abc.ABC):

    def update_user(
            self,
            battletag: str,
            data: dict
    ):
        key = self._make_user_key(battletag)
        self.set(
            key,
            data
        )

    def get_user_stats(
            self,
            battletag: str,
    ):
        key = self._make_user_key(battletag)
        return self.get(key)

    def _make_user_key(self, battletag):
        return "user:{}".format(
            battletag,
        )

    @abc.abstractmethod
    def get(self, key: str) -> dict:
        pass

    @abc.abstractmethod
    def set(self, key: str, mapping: dict):
        pass

    @abc.abstractmethod
    def keys(self):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def delete(self, key):
        pass


class LocMemStorage(Storage):

    def __init__(self):
        self._hashmaps = {}

    def set(self, key: str, mapping: dict) -> None:
        self._hashmaps[key] = mapping

    def get(self, key: str) -> dict:
        return self._hashmaps.get(key, {})

    def keys(self):
        return self._hashmaps.keys()

    def clear(self):
        self._hashmaps = {}

    def delete(self, key):
        self._hashmaps.pop(key, None)

    @property
    def redis(self) -> dict:
        return self._hashmaps


class RedisStorage(Storage):
    def __init__(self, url):
        self._redis = redis.from_url(url)
        super().__init__()

    def set(self, key: str, mapping: dict) -> bool:
        return self.redis.hmset(key, mapping)

    def get(self, key: str) -> dict:
        return self.redis.hgetall(key)

    def keys(self) -> List[str]:
        return self.redis.keys()

    def clear(self):
        pass

    def delete(self, key):
        self.redis.delete(key)

    @property
    def redis(self):
        return self._redis


def init_storage():
    redis_class = REDIS_CLASS[ENVIRONMENT]["CLASS"]
    params = REDIS_CLASS[ENVIRONMENT].get('OPTIONS', {})

    storage_cls = import_string(redis_class)
    return storage_cls(**params)

redis_storage = init_storage()