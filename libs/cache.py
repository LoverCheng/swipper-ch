from pickle import dumps, loads, HIGHEST_PROTOCOL, UnpicklingError

from redis import Redis as _Redis

from swiper.config import REDIS


class Redis(_Redis):
    '''带 Pickle 处理的 Redis 类'''

    def set(self, name, value, ex=None, px=None, nx=False, xx=False, keepttl=False):
        '''
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.
        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.
        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.
        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.
        ``keepttl`` if True, retain the time to live associated with the key.
            (Available since Redis 6.0)
        '''
        # 将 value 序列化处理
        pickled_value = dumps(value, HIGHEST_PROTOCOL)
        return super().set(name, pickled_value, ex, px, nx, xx, keepttl)

    def get(self, name, default=None):
        '''Return the value at key ``name``, or None if the key doesn't exist'''
        pickled_value = super().get(name)

        if pickled_value is None:
            return default

        try:
            return loads(pickled_value)
        except UnpicklingError:
            return pickled_value


rds = Redis(**REDIS)
