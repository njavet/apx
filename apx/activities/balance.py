# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = Balance

    def post_saving(self, user_id):
        user = db.User.select().where(db.User.user_id == user_id).get()
        user.weight = self.activity.weight
        user.save()


class Balance(db.ActivityUnit):
    weight = pw.FloatField()
    fat = pw.FloatField(null=True)
    water = pw.FloatField(null=True)
    muscles = pw.FloatField(null=True)

    def parse_and_save(self, payload):
        try:
            self.weight = float(payload[0])
        except (IndexError, ValueError):
            raise exceptions.ActivityProcessingError('Specify the weight')
        try:
            self.fat = float(payload[1])
        except (IndexError, ValueError):
            self.fat = None
        try:
            self.water = float(payload[2])
        except (IndexError, ValueError):
            self.water = None
        try:
            self.muscles = float(payload[3])
        except (IndexError, ValueError):
            self.muscles = None
