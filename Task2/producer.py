import random
import pika
from faker import Faker
import pika.spec

from config.model import Contact
from config.config import connection, channel, connect
from config.decorators import error_decorator


faker = Faker("en_US")


@error_decorator
def seed_contacts(qty):
    for _ in range(qty):
        contact = Contact(
            fullname=faker.name(),
            email=faker.email(),
            phone=faker.phone_number(),
            date_notify="...",
            message_method=random.choice(["email", "sms"]),
        )
        contact.save()
        yield contact


def send_to_queue(contacts: list):
    queue_email = "email"
    queue_sms = "sms"
    exchange = "web25_exchange"

    channel.exchange_declare(exchange=exchange, exchange_type="direct")
    channel.queue_declare(queue=queue_email, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue_email)

    channel.queue_declare(queue=queue_sms, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue_sms)

    for contact in contacts:
        if contact.message_method == "email":
            iqueue = queue_email
        else:
            iqueue = queue_sms
        channel.basic_publish(
            exchange=exchange,
            routing_key=iqueue,
            body=str(contact.id).encode("utf-8"),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
        )
        print(f"Sent contact ID to queue: {contact.id}")
    connection.close()


if __name__ == "__main__":
    qty_contact = 10
    contact_ids = list(seed_contacts(qty_contact))
    send_to_queue(contact_ids)
    # test(contact_ids)
