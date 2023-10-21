# general imports

# project imports
from apx import db


class ActivityProcessor:
    def __init__(self):
        self.activity = None
        self.activity_model = None

    def process_activity(self, user_id, emoji, words,
                         recv_time=None,
                         unit_name=None,
                         comment=None):
        self.init_activity_unit(user_id, emoji, unit_name, comment)
        self.activity.set_time(recv_time)
        self.parse_and_save(words)

    def init_activity_unit(self, user_id, emoji, name=None, comment=None):
        self.activity = self.activity_model(user=user_id,
                                            emoji=emoji,
                                            comment=comment)
        if name:
            self.activity.name = name

    def parse_and_save(self, words):
        self.activity.parse(words)
        self.activity.save()

    def post_saving(self, user_id):
        pass

