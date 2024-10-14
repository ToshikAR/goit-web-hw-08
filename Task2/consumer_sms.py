import os
import sys
from datetime import datetime

from config.model import Contact
from config.config import channel, connect


def main():
    queue = "sms"
    channel.queue_declare(queue=queue, durable=True)
    # ---------------------------------------------------------------------

    def callback(ch, method, properties, body):
        contact_id = body.decode()
        contact = Contact.objects(id=contact_id, message_method=queue).first()
        if contact and not contact.sms_sent:
            contact.sms_sent = True
            contact.date_notify = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            contact.save()
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # ---------------------------------------------------------------------
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
