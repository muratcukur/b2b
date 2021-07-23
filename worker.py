import os
from urllib.parse import urlparse
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = urlparse(os.environ.get('REDISTOGO_URL', 'redis://localhost:6959'))

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
        }
    }
}

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()