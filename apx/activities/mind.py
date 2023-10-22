# general imports
import peewee as pw
import datetime
import re

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
            self.activity.parse_and_set_time_string(words[0])
        except IndexError:
            raise exceptions.ActivityProcessingError('specify time')
        try:
            self.activity.topic = words[1]
        except IndexError:
            raise exceptions.ActivityProcessingError('specify topic')
        self.activity.save()

