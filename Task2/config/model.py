from mongoengine import BooleanField, StringField, Document, ListField


class Contact(Document):
    fullname = StringField(max_length=120, required=True)
    email = StringField(max_length=254, required=True)
    email_sent = BooleanField(default=False)
    date_notify = StringField(max_length=120, required=True)

