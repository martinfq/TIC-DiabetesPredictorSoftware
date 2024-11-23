import redis
import os
from dotenv import load_dotenv

def redis_connection():
    try:
        load_dotenv()
        host = os.getenv('DB_HOST')
        port = os.getenv('DB_PORT')
        return redis.Redis(
            host=host,
            port=port,
            decode_responses=True
            )
    except:
        print('error in the connection')