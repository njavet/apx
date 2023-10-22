import unittest

import peewee as pw
from apx.db import ChronoUnit
from apx.activities.mind import ActivityProcessor
from apx.utils import exceptions

test_db = pw.SqliteDatabase(':memory:')
test_user_id = 101

MODELS = [ChronoUnit]


class TestBalance(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.emoji = b'\xf0\x9f\x93\xa1'.decode()
        self.ap = ActivityProcessor()

    def tearDown(self) -> None:
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_complete_input(self):
        self.ap.process_activity(test_user_id,
                                 self.emoji,
                                 ['60', 'AI'],
                                 unit_name='study')
        self.assertEqual(self.ap.activity.seconds, 3600)
        self.assertEqual(self.ap.activity.topic, 'AI')

    def test_invalid_weight(self):
        with self.assertRaises(exceptions.ActivityProcessingError) as context:
            self.ap.process_activity(test_user_id,
                                     self.emoji,
                                     ['cyborg'],
                                     unit_name='study')


if __name__ == '__main__':
    unittest.main()


