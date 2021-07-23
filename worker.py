import os
import redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = os.getenv('REDISTOGO_URL', 'redis://redistogo:9eaca0616a5dba0da432cbae5b3ae40b@soapfish.redistogo.com:11585/')

CACHES = {
        'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'OPTIONS': {
            'DB': 0,   # or 1?
            #'PARSER_CLASS': 'redis.connection.HiredisParser'
        },
    },
 }

CELERY_RESULT_BACKEND = redis_url
BROKER_URL = 'redis://redistogo:9eaca0616a5dba0da432cbae5b3ae40b@soapfish.redistogo.com:11585/'

conn = redis.from_url(redis_url)


if __name__ == '__main__':
    with Connection(conn):
        print('Launching redis worker...')
        worker = Worker(map(Queue, listen))
        worker.work()