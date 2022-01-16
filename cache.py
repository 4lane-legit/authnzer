import redis

redis_ins = redis.Redis(host='host.docker.internal', port=6379, db=0,  charset="utf-8", decode_responses=True)