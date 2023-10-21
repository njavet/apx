# general imports

# project imports
from apx import db


class ActivityProcessor:
    def __init__(self):
        self.activity = None
        self.activity_model = None

    def process_activity(self, words):
        try:
            self.activity.parse_and_save(words)
        except ApxError as ae:
            return ae.msg

    def init_activity_unit(self, user_id, emoji, name=None, comment=None):
        self.activity = self.activity_model(user=user_id,
                                            emoji=emoji,
                                            comment=comment)
        if name:
            self.activity.name = name

    def post_saving(self, user_id):
        pass


class ApxError(Exception):
    def __init__(self, msg=None):
        self.msg = msg
