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
            date_notify="...",
        )
        contact.save()
        yield str(contact.id)


def send_to_queue(contact_ids: list):
    queue_email = "email"
    exchange = "web25_exchange"

    channel.exchange_declare(exchange=exchange, exchange_type="direct")
    channel.queue_declare(queue=queue_email, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue_email)

    for contact_id in contact_ids:
        channel.basic_publish(
            exchange=exchange,
            routing_key=queue_email,
            body=contact_id.encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            ),
        )
        print(f"Sent contact ID to queue: {contact_id}")
    connection.close()


if __name__ == "__main__":
    qty_contact = 3
    contact_ids = list(seed_contacts(qty_contact))
    send_to_queue(contact_ids)
