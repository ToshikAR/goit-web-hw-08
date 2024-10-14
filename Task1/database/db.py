import os
import redis

from redis_lru import RedisLRU

from mongoengine import connect
from dotenv import load_dotenv


# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

load_dotenv()
user = os.getenv("MONGODB08_USER")
password = os.getenv("MONGODB08_PASSWORD")
base = os.getenv("MONGODB08_DB")
domain = os.getenv("MONGODB08_HOST")

# uri = (
#     f"mongodb+srv://{user}:{password}@{domain}/{base}?retryWrites=true&w=majority&appName=Cluster0"
# )
# client = MongoClient(uri, server_api=ServerApi("1"))
# db = client[base]


# connect to AtlasDB
connect(
    db=base,
    host=f"mongodb+srv://{user}:{password}@{domain}/?retryWrites=true&w=majority&appName=Cluster0",
)

rb_host = os.getenv("REDIS_M08_HOST")
rb_port = os.getenv("REDIS_M08_PORT")
rb_password = os.getenv("REDIS_M08_PASSWORD")

# connect to Redis
client_redis = redis.StrictRedis(host=rb_host, port=rb_port, password=None)
cache_redis = RedisLRU(client_redis)
