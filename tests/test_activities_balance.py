import unittest

import peewee as pw
from apx.activities.balance import ActivityProcessor, Balance
from apx.utils import exceptions

test_db = pw.SqliteDatabase(':memory:')
test_user_id = 101

MODELS = [Balance]


class TestBalance(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.emoji = b'\xe2\x9a\x96\xef\xb8\x8f'.decode()
        self.ap = ActivityProcessor()

    def tearDown(self) -> None:
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_complete_input(self):
        self.ap.process_activity(test_user_id,
                                 self.emoji,
                                 ['101', '16.1', '60', '42'])
        self.assertEqual(self.ap.activity.weight, 101)
        self.assertEqual(self.ap.activity.fat, 16.1)
        self.assertEqual(self.ap.activity.water, 60)
        self.assertEqual(self.ap.activity.muscles, 42)

    def test_weight_only(self):
        self.ap.process_activity(test_user_id,
                                 self.emoji,
                                 ['98.5'])
        self.assertEqual(self.ap.activity.weight, 98.5)
        self.assertIsNone(self.ap.activity.fat)
        self.assertIsNone(self.ap.activity.water)
        self.assertIsNone(self.ap.activity.muscles)

    def test_invalid_weight(self):
        with self.assertRaises(exceptions.ActivityProcessingError) as context:
            self.ap.process_activity(test_user_id,
                                     self.emoji,
                                     ['10f', '16.1', '60', '42'])


if __name__ == '__main__':
    unittest.main()


