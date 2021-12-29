import unittest

from main import path
from migrations.db_conn import Database


class TestTodo(unittest.TestCase):
    def setUp(self):
        self.db = Database(path)

    def test_addtodo(self):
        pass

    def test_addrepotodo(self):
        pass

    def test_markascomplete(self):
        pass

    def test_deltodo(self):
        pass
