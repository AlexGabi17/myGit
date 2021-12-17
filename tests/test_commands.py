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
        def test_input(id: int, token: str, chat_id: int):
            self.mock_update.message.text = "/set " + token
            self.mock_update.message.from_user.id = id
            self.mock_update.message.chat_id = chat_id

        # Setup args
        input = (12344, "2342134324", 1)
        test_input(input[0], input[1], input[2])

        # Call function
        setUser(self.mock_update, Mock())

       # Check the data in the database
        rows = self.db.select('users', input[0])
        self.assertNotEqual(rows, [])
        self.assertEqual(rows[0], (input[0], input[1]))

    def test_getRepos(self):
        pass

    def test_setRepo(self):
        pass

    def test_issues(self):
        pass
