import unittest
from unittest.mock import Mock

from sqlite3 import Error
from main import path, setRepoInChat, setUser
from migrations.db_conn import Database


class TestCommand(unittest.TestCase):
    def setUp(self):
        self.mock_update = Mock()
        self.mock_update.message = Mock()
        self.mock_update.message.text = "test"

        self.db = Database(path)

    def clean_from_db(self, table: str, id: int):
        query = f"""
            DELETE FROM {table} 
            WHERE id={id}
        """
        self.db.exec_query(query)

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
        rows = self.db.select("users", input[0])
        self.assertNotEqual(rows, [])
        self.assertEqual(rows[0], (input[0], input[1]))

        # Cleanup
        self.clean_from_db("users", input[0])

    def test_setRepo(self):
        def test_input(id: int, chat_id: int, repo_name: str):
            self.mock_update.message.text = "/setrepo " + repo_name
            self.mock_update.message.from_user.id = id
            self.mock_update.message.chat_id = chat_id

        # Setup args
        user_id = 123444
        chat_id = -1
        repo_name = "mstanciu552/dotfiles"
        token = "12314512341"

        test_input(user_id, chat_id, repo_name)

        # Check if the user_id is present
        res = self.db.select("users", user_id)

        # Insert into users table if not already
        if res == []:
            self.db.insert("users", {"id": str(user_id), "token": token})

            # Get user based on id
            res = self.db.select("users", user_id)

        # Assertions about the users table
        self.assertNotEqual(res, [])
        self.assertEqual(res[0], (user_id, token))

        # Call function
        func = setRepoInChat(self.mock_update, Mock())

        # Test if the github token is invalid
        self.assertEqual(func, -1)
        if func == -1:
            return

        # Final Assertions
        result = self.db.select("groups", chat_id)

        self.assertEqual(result, [])
        self.assertNotEqual(result[0], (user_id, repo_name))

        # Cleanup
        self.clean_from_db("users", user_id)
        self.clean_from_db("groups", user_id)
