# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = Gym


class Gym(db.ChronoUnit):

    def parse(self, words):
        try:
            self.parse_start_end_time(words[0])
        except IndexError:
            raise exceptions.ActivityProcessingError('Specify the start and end time of the unit!')
        self.seconds = (self.end - self.start).seconds
        try:
            self.place = words[1]
        except IndexError:
            pass


database = pw.SqliteDatabase(db.DB_NAME)
database.connect()
database.create_tables([Gym], safe=True)
database.close()
