from datetime import datetime

from config.model import Contact
from config.config import channel, connect
from config.decorators import error_decorator


def main():
    queue_email = "email"
    channel.queue_declare(queue=queue_email, durable=True)
    # ---------------------------------------------------------------------

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        contact = Contact.objects(id=contact_id).first()
        if contact and not contact.email_sent:
            contact.email_sent = True
            contact.date_notify = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            contact.save()
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # ---------------------------------------------------------------------
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_email, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
