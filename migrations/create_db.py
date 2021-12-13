from db_conn import Database
db = Database("db/myGit.sqlite")
create_user_table = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        token TEXT NOT NULL
    )
"""
db.exec_query(create_user_table)
