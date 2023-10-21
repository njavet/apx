import unittest

import peewee as pw

from apx.activities.wimhof import ActivityProcessor, Wimhof, Round

test_db = pw.SqliteDatabase(':memory:')
test_user_id = 101

MODELS = [Wimhof, Round]


class TestWimhof(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)
        self.emoji = b'\xf0\x9f\xaa\x90'.decode()
        self.ap = ActivityProcessor()

    def tearDown(self) -> None:
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_valid_activity(self):
        payload = '30 120 30 150 30 180'.split()
        self.ap.process_activity(test_user_id, self.emoji, payload)
        self.assertEqual(self.ap.rounds[0].retention, 120)


if __name__ == '__main__':
    unittest.main()


