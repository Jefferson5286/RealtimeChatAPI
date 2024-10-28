from exceptions import CacheConfirmKeyNotFound, IncorrectCacheType

from cachetools import TTLCache


class Caching:
    def __init__(self):
        self._cache = {
            'confirm': TTLCache(maxsize=10, ttl=600)
        }
        self._cache_types = self._cache.keys()

    def get(self, cache: str, value: str):
        """
            Pega um cache, e o deleta assim que for encontrado e retornado.

            :param cache: Tipo de cache;
            :param value: Key alvo do cache.

            :raise CacheConfirmKeyNotFound: Caso não seja encontrada a key, retornará um erro de existence;
            :raise IncorrectCacheType: Tipo de cache buscado não encontrado.
        """
        if cache not in self._cache_types:
            raise IncorrectCacheType

        if value not in self._cache[cache].keys():
            raise CacheConfirmKeyNotFound

        cache = self._cache[cache]

        del self._cache[cache]

        return cache[value]
