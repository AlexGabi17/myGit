import os
import unittest
from migrations.db_conn import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.path = "tests/db/test.sqlite"
        self.db = Database(self.path)

    # Cleanup
    def tearDown(self):
        clear_table_query = """
            DROP TABLE IF EXISTS users;
        """
        self.db.exec_query(clear_table_query)

        if os.path.exists(self.path):
          os.remove(self.path)


    def test_init(self):
        # Create users table
        create_user_table = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                token TEXT NOT NULL
            )
        """
        self.db.exec_query(create_user_table)

        # Check if the table exists
        self.db.cursor.execute(f'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'users\'')
        self.assertNotEqual(self.db.cursor.fetchall(), [])
        
    def test_insert(self):
        # Create users table
        create_user_table = """
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                token TEXT NOT NULL
            )
        """
        self.db.exec_query(create_user_table)

        # Test inserting into the database
        self.db.insert('users', {'id': '320', 'token': '124234234'})
        row = self.db.select('users', 320)

        self.assertNotEqual(row, [])

        # Test selecting data from the database
        self.assertEqual(row[0], (320, '124234234')) 
