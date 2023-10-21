# general imports
import peewee as pw

# project imports
from apx import db
from apx.utils import exceptions
from . import base


class ActivityProcessor(base.ActivityProcessor):
    def __init__(self):
        super().__init__()
        self.activity_model = Wimhof
        self.rounds = []

    def parse_and_save(self, words):
        self.rounds = []
        breaths = [int(b) for b in words[::2]]
        retentions = [float(r) for r in words[1::2]]
        if len(breaths) != len(retentions):
            raise exceptions.ActivityProcessingError('Not the same number of breaths and seconds')
        if len(breaths) < 1:
            raise exceptions.ActivityProcessingError('At least one round necessary')
        self.activity.save()

        for i, (b, r) in enumerate(zip(breaths, retentions)):
            r = Round(activity_unit=self.activity.get_id(),
                      round_nr=i,
                      breaths=b,
                      retention=r)
            r.save()
            self.rounds.append(r)


class Wimhof(db.ActivityUnit):

    def parse(self, words):
        pass


class Round(db.SubUnit):
    round_nr = pw.IntegerField()
    breaths = pw.IntegerField()
    retention = pw.IntegerField()


database = pw.SqliteDatabase(db.DB_NAME)
database.connect()
database.create_tables([Wimhof, Round], safe=True)
database.close()
