import unittest
from unittest.mock import Mock
from main import path, setUser
from migrations.db_conn import Database

class TestCommand(unittest.TestCase):

    def setUp(self):
        self.mock_update = Mock()
        self.mock_update.message = Mock()
        self.mock_update.message.text = "test"

        self.db = Database(path)

    def tearDown(self):
        pass

    def test_set(self):
        # Setup args
        temp_id = 12344
        token = "1212413242342"

        self.mock_update.message.text = "/set " + token
        self.mock_update.message.from_user.id = temp_id
        self.mock_update.message.chat_id = 1
        mock_context = Mock()

        # Call function
        setUser(self.mock_update, mock_context)

        # Check the data in the database
        rows = self.db.select('users', temp_id)
        self.assertNotEqual(rows, [])
        self.assertEqual(rows[0], (temp_id, token))

    def test_getRepos(self):
        pass

    def test_setRepo(self):
        pass

    def test_issues(self):
        pass
