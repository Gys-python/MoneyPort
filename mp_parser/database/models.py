from datetime import datetime
from peewee import *
from settings.settings import *


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


class QuestionMessage(BaseModel):
    message_id = BigIntegerField(unique=True)
    date = DateTimeField()
    user_id = BigIntegerField()
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    text = TextField()


class AnswerMessage(BaseModel):
    message_id = BigIntegerField(unique=True)
    date = DateTimeField()
    user_id = BigIntegerField()
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    text = TextField()
    question_id = ForeignKeyField(QuestionMessage, backref='answers', null=True)
    reply_to_msg_id = BigIntegerField()


class LastParsed(BaseModel):
    last_parsed_id = BigIntegerField(default=0)


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


db.create_tables([QuestionMessage, AnswerMessage, LastParsed], safe=True)