import redis

redis_ins = redis.Redis(host='host.docker.internal', port=6379, db=0)