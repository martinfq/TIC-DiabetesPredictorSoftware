import redis

def redis_connection():
    try:
        return redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True
            )
    except:
        print('error in the connection')