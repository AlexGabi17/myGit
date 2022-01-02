import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self, path):
        self.path = path
        try:
            self.connection = sqlite3.connect(path, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def select(self, table: str, id=None):
        query = f"SELECT * FROM '{table}'"
        if id:
            query += f"WHERE id = {str(id)}"
        query += ";"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def select_order(self, table: str, order: dict = None, id=None):
        query = f"SELECT * FROM '{table}'"
        if id:
            query += f"WHERE id = {str(id)}"

        if order:
            query += " ORDER BY "
            for key, value in order.items():
                query += f"{key} {value},"
            query = query[:-1]
        query += ";"

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert(self, table, data):
        if not data:
            raise Error("Wrong data format")

        fields = ""
        values = "'"
        for key, value in data.items():
            fields += key + ","
            values += str(value) + "','"

        fields = fields[: len(fields) - 1]
        values = values[: len(values) - 2]

        query = f"INSERT INTO {table}({fields}) VALUES({values})"
        self.cursor.execute(query)
        self.connection.commit()

    def update(self, table: str, data: dict, id: str):
        if not data or table == "":
            return
        query = f"UPDATE {table} SET "
        for key, value in data.items():
            query += f'{key} = "{value}",'
        query = query[:-1]
        query += f" WHERE id={id};"

        self.exec_query(query)

    def update_like(self, table: str, data: dict, id: str, like: dict):
        if not data or table == "":
            return
        query = f"UPDATE {table} SET "
        for key, value in data.items():
            query += f'{key} = "{value}",'
        query = query[:-1]

        query += " WHERE"

        for key, value in like.items():
            query += f" {key} LIKE '{value}%' AND"
        query += f" id={id};"

        self.exec_query(query)

    def delete(self, table: str, id: int):
        if not id:
            return

        delete_query = f"""
            DELETE FROM {table} 
            WHERE id = {str(id)}
        """
        self.cursor.execute(delete_query)
        self.connection.commit()

    def delete_like(self, table: str, id: int, like: dict):
        if not id:
            return

        delete_query = f"DELETE FROM {table}"

        delete_query += " WHERE"

        for key, value in like.items():
            delete_query += f" {key} LIKE '{value}%' AND"

        delete_query += f" id={str(id)};"

        self.exec_query(delete_query)

    def update_user_token(self, data):
        if not data or not data["id"]:
            raise Error("Wrong data format")
        query = f"UPDATE users SET "

        query += f'token = "{str(data["token"])}" '

        query += f' WHERE id = {str(data["id"])};'
        # print(query)
        self.cursor.execute(query)
        self.connection.commit()

    def update_group_repo(self, data):
        if not data or not data["id"]:
            raise Error("Wrong data format")
        query = f'UPDATE groups SET repo = "{str(data["repo"])}" WHERE id = {str(data["id"])} ;'

        self.cursor.execute(query)
        self.connection.commit()

    def exec_query(self, query: str):
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            raise Error("Query Error", e)
