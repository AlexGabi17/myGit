import os
import unittest
from migrations.db_conn import Database

class TestDatabase(unittest.TestCase):

    # Cleanup
    def clean(self, db):
        clear_table_query = """
            DROP TABLE IF EXISTS users;
        """
        db.exec_query(clear_table_query)

        if os.path.exists("tests/db/test.sqlite"):
          os.remove("tests/db/test.sqlite")


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

        self.clean(db)
        
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

        # Test inserting into the database
        db.insert('users', {'id': '320', 'token': '124234234'})
        row = db.select('users', 320)

        self.assertNotEqual(row, [])

        # Test selecting data from the database
        self.assertEqual(row[0], (320, '124234234')) 

        self.clean(db)
