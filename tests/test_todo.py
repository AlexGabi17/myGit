import unittest
from unittest.mock import Mock

from main import addTodo, path
from migrations.db_conn import Database
from datetime import datetime


class TestTodo(unittest.TestCase):
    def setUp(self):
        self.db = Database(path)
        self.mock_update = Mock()
        self.mock_update.message = Mock()

    def test_addtodo(self):
        def test_input(id: int, task: str, date: str):
            self.mock_update.message.text = f"/addtodo {task} {date}"
            self.mock_update.message.from_user.id = id

        test_id = 5012312321
        task_name = "testing spaces"
        task_date = ""
        date_now = datetime.today().strftime("%Y-%m-%d")

        test_input(test_id, task_name, task_date)

        addTodo(self.mock_update, Mock())

        todos = self.db.select("todos", test_id)
        self.db.delete("todos", test_id)
        self.assertNotEqual(todos, [])
        self.assertEquals(todos[0], (test_id, "NULL", task_name, None, date_now, 0))

    def test_addrepotodo(self):
        pass

    def test_markascomplete(self):
        pass

    def test_deltodo(self):
        pass
