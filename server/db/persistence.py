from peewee import *
import datetime
from enum import Enum
from peewee import *
import datetime


class EventType(Enum):
    UPLOAD = "upload"
    PROCESSED = "processed"
    FAILED = "failed"

db = SqliteDatabase('events.db')

class BaseModel(Model):
    class Meta:
        database = db

class Events(BaseModel):
    filename = CharField(unique=True)
    uploaded_date = DateTimeField(default=datetime.datetime.now)
    status = CharField()
    username = CharField()

db.connect()
db.create_tables([Events])

class Persistence:
    @staticmethod
    def create_tables():
        db.connect()
        db.create_tables([Events])

    @staticmethod
    def create_event(filename, status:EventType, username):
        event = Events(filename=filename, status=status.value, username=username)
        event.save()
    
    @staticmethod
    def get_events():
        for event in Events.select().order_by(Events.uploaded_date.desc()):
            print(event.filename, event.status, event.uploaded_date, event.username) 
                                              

    





    
