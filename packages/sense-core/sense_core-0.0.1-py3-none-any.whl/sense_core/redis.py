import redis
from .config import config

__client_map = {}


def get_redis_client(db=0, label='redis'):
    """
    @rtype: StrictRedis
    """
    redis_host = config(label,'host')
    redis_port = config(label,'port')
    redis_pass = config(label,'pass')
    if len(redis_pass) == 0:
        redis_pass = None
    global __client_map
    if label not in __client_map:
        redis_pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, db=db)
        clients = redis.Redis(connection_pool=redis_pool)
        __client_map[label] = clients

    return __client_map[label]
