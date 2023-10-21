# general imports
import datetime
import peewee as pw


DB_NAME = 'activities.db'


class BaseModel(pw.Model):
    class Meta:
        database = pw.SqliteDatabase(DB_NAME)


class User(BaseModel):
    user_id = pw.IntegerField(primary_key=True)
    user_name = pw.CharField(default='Platon')
    age = pw.IntegerField(null=True)
    weight = pw.FloatField(null=True)
    height = pw.FloatField(null=True)


class ActivityUnit(BaseModel):
    user = pw.ForeignKeyField(User)
    emoji = pw.CharField()
    log_time = pw.DateTimeField()
    # a unit that is logged after midnight before sleeping
    # should count for the last day 0400-0359 is the day then
    log_date = pw.DateField()
    comment = pw.TextField(null=True)

    def set_time(self, recv_time):
        if recv_time is None:
            self.log_time = datetime.datetime.now()
        else:
            self.log_time = recv_time

        if datetime.time(0) < self.log_time.time() < datetime.time(3):
            # should count for the last day
            self.log_date = self.log_time.date() - datetime.timedelta(days=1)
        else:
            self.log_date = self.log_time.date()

    def parse_and_save(self, payload):
        raise NotImplementedError


class ChronoUnit(ActivityUnit):
    seconds = pw.IntegerField()
    start = pw.DateTimeField(null=True)
    end = pw.DateTimeField(null=True)
    place = pw.CharField(null=True)
    effort = pw.IntegerField(default=3)
