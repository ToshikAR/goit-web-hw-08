import os
import pika
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()

# connect to RabbitMQ
user = os.getenv("RABBITMQ_M08_USER")
password = os.getenv("RABBITMQ_M08_PASS")
port = os.getenv("RABBITMQ_M08_PORT_R")
host = os.getenv("RABBITMQ_M08_HOST")

credentials = pika.PlainCredentials(user, password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host, port=port, credentials=credentials)
)
channel = connection.channel()


# connect to AtlasDB
user_mongo = os.getenv("MONGODB08_USER")
password_mongo = os.getenv("MONGODB08_PASSWORD")
base_mongo = os.getenv("MONGODB08_DB")
domain_mongo = os.getenv("MONGODB08_HOST")

connect(
    db=base_mongo,
    host=f"mongodb+srv://{user_mongo}:{password_mongo}@{domain_mongo}/?retryWrites=true&w=majority&appName=Cluster0",
)
