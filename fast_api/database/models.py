from peewee import *
from mp_parser.settings.settings import DATABASE, USER, PASSWORD, HOST, PORT
from datetime import datetime

db = PostgresqlDatabase(
    database=DATABASE,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    autorollback=True,
    autoconnect=True,
)


class BaseModel(Model):
    class Meta:
        database = db


class FilteredMessage(BaseModel):
    message_id = BigIntegerField(primary_key=True)
    date = DateTimeField(default=datetime.now)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    text = TextField()
    answers = TextField(null=True)

    class Meta:
        table_name = 'filtered_messages'

db.connect()
db.create_tables([FilteredMessage], safe=True)
