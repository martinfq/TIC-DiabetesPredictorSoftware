import redis

def redis_connection():
    try:
        return redis.StrictRedis(
            host='redis-11440.c81.us-east-1-2.ec2.redns.redis-cloud.com',
            port=11440,
            password='tesis',
            decode_responses=True
            )
    except:
        print('error in the connection')