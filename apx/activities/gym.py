# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = db.ChronoUnit

    def parse_and_save(self, words):
        try:
            self.activity.parse_and_set_start_end_time(words[0])
        except IndexError:
            raise exceptions.ActivityProcessingError('Specify the start and end time of the unit!')
        self.activity.seconds = (self.activity.end - self.activity.start).seconds
        try:
            self.activity.place = words[1]
        except IndexError:
            raise exceptions.ActivityProcessingError('Specify the gym')
        self.activity.save()
