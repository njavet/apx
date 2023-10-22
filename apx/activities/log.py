# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = Log

    def post_saving(self, user_id):
        user = db.User.select().where(db.User.user_id == user_id).get()
        user.weight = self.activity.weight
        user.save()


class Log(db.ActivityUnit):
    unit_name = pw.CharField()
    log = pw.CharField()

    def parse(self, words):
        try:
            self.log = words[0]
        except IndexError:
            raise exceptions.ActivityProcessingError('Specify the log')


database = pw.SqliteDatabase(db.DB_NAME)
database.connect()
database.create_tables([Log], safe=True)
database.close()
