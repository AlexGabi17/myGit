import unittest
from migrations.db_conn import Database

class TestDatabase(unittest.TestCase):
    def test_init(self):
        # Create users table
        db = Database("tests/db/test.sqlite")
        create_user_table = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                token TEXT NOT NULL
            )
        """
        db.exec_query(create_user_table)

        # Check if the table exists
        db.cursor.execute(f'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'users\'')
        self.assertNotEqual(db.cursor.fetchall(), [])

    def test_insert(self):
        # Create users table
        db = Database("tests/db/test.sqlite")
        create_user_table = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                token TEXT NOT NULL
            )
        """
        db.exec_query(create_user_table)
        db.insert('users', {'id': 320, 'token': '124234234'})
        self.assertNotEqual(db.select('users', 320), [])



