import unittest

import peewee as pw
from apx.db import ChronoUnit
from apx.activities.chrono import ActivityProcessor
from apx.utils import exceptions

test_db = pw.SqliteDatabase(':memory:')
test_user_id = 101

MODELS = [ChronoUnit]


class TestBalance(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.emoji = b'\xe2\x9a\x94\xef\xb8\x8f'.decode()
        self.ap = ActivityProcessor()

    def tearDown(self) -> None:
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_valid_min_sec(self):
        self.ap.process_activity(test_user_id,
                                 self.emoji,
                                 ['16:05'],
                                 unit_name='splitmachine')
        self.assertEqual(self.ap.activity.seconds, 965)
        self.assertEqual(self.ap.activity.unit_name, 'splitmachine')

    def test_valid_min(self):
        self.ap.process_activity(test_user_id,
                                 self.emoji,
                                 ['16'],
                                 unit_name='splitmachine')
        self.assertEqual(self.ap.activity.seconds, 960)
        self.assertEqual(self.ap.activity.unit_name, 'splitmachine')

    def test_invalid_time(self):
        with self.assertRaises(exceptions.ActivityProcessingError) as context:
            self.ap.process_activity(test_user_id,
                                     self.emoji,
                                     ['10f'],
                                     unit_name='splitmachine')


if __name__ == '__main__':
    unittest.main()


