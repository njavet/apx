import unittest

import peewee as pw

from apx.db import User
from apx.activities.lifting import ActivityProcessor, Lifting, Set

test_db = pw.SqliteDatabase(':memory:')
test_user_id = 101

MODELS = [User, Lifting, Set]


class TestSquat(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        User.create(user_id=test_user_id, name='Schopenhauer')
        self.emoji = b'\xe2\x9b\xa9\xef\xb8\x8f'.decode()
        self.ap = ActivityProcessor()

    def tearDown(self) -> None:
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_valid_activity(self):
        payload = '100 10 180 110 8 240 120 4'.split()
        self.ap.process_activity(test_user_id, self.emoji, payload, unit_name='squat')
        self.assertEqual(self.ap.sets[0].weight, 100)


if __name__ == '__main__':
    unittest.main()


