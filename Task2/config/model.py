from mongoengine import BooleanField, StringField, Document, ListField


class Contact(Document):
    fullname = StringField(max_length=120, required=True)
    email = StringField(max_length=254, required=True)
    phone = StringField(max_length=50, required=True)
    email_sent = BooleanField(default=False)
    sms_sent = BooleanField(default=False)
    date_notify = StringField(max_length=120, required=True)
    message_method = StringField(choices=["email", "sms"], required=True)

