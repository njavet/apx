# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions, utilities
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = Lifting
        self.sets = []

    def parse_and_save(self, words):
        self.sets = []
        weights = [float(w) for w in words[::3]]
        reps = [float(r) for r in words[1::3]]
        pauses = [float(p) for p in words[2::3]] + [0]

        if len(reps) != len(weights):
            raise exceptions.ActivityProcessingError('Not the same number of reps and weights')
        if len(pauses) != len(reps):
            raise exceptions.ActivityProcessingError('break error')
        if len(reps) < 1:
            raise exceptions.ActivityProcessingError('No set')

        at = db.User.select().where(db.User.user_id == self.activity.user_id).get()
        self.activity.save()

        for i, (w, r, b) in enumerate(zip(weights, reps, pauses)):
            orm = utilities.estimate_orm(w, r)
            try:
                rel_strength = orm / at.weight
            except TypeError:
                rel_strength = None
            ls = LiftSet(activity_unit=self.activity.get_id(),
                         set_nr=i,
                         weight=w,
                         reps=r,
                         pause=b,
                         orm=orm,
                         rel_strength=rel_strength)
            ls.save()
            self.sets.append(ls)


class Lifting(db.ActivityUnit):
    unit_name = pw.CharField()

    def parse(self, words):
        pass


class LiftSet(db.SubUnit):
    set_nr = pw.IntegerField()
    weight = pw.FloatField()
    reps = pw.FloatField()
    pause = pw.IntegerField()
    orm = pw.FloatField()
    rel_strength = pw.FloatField(null=True)


database = pw.SqliteDatabase(db.DB_NAME)
database.connect()
database.create_tables([Lifting, LiftSet], safe=True)
database.close()
