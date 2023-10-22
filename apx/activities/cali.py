# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = Cali
        self.sets = []

    def parse_and_save(self, words):
        self.sets = []
        reps = [float(r) for r in words[::2]]
        pauses = [float(p) for p in words[1::2]] + [0]
        at = db.User.select().where(db.User.user_id == self.activity.user_id).get()
        weights = len(reps) * [at.weight]

        if len(pauses) != len(reps):
            raise exceptions.ActivityProcessingError('break error')
        if len(reps) < 1:
            raise exceptions.ActivityProcessingError('No set')
        self.activity.save()

        for i, (w, r, b) in enumerate(zip(weights, reps, pauses)):
            ls = CaliSet(activity_unit=self.activity.get_id(),
                         set_nr=i,
                         weight=w,
                         reps=r,
                         pause=b)
            ls.save()
            self.sets.append(ls)


class Cali(db.ActivityUnit):
    unit_name = pw.CharField()

    def parse(self, words):
        pass


class CaliSet(db.SubUnit):
    set_nr = pw.IntegerField()
    weight = pw.FloatField(null=True)  # bodyweight
    reps = pw.FloatField()
    pause = pw.IntegerField()


database = pw.SqliteDatabase(db.DB_NAME)
database.connect()
database.create_tables([Cali, CaliSet], safe=True)
database.close()
