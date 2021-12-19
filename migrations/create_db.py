from db_conn import Database

db = Database("db/myGit.sqlite")
create_user_table = """
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        token TEXT NOT NULL
    )
"""
db.exec_query(create_user_table)
create_group_table = """
    CREATE TABLE IF NOT EXISTS groups(
        id INTEGER PRIMARY KEY,
        repo TEXT NOT NULL
    )
"""
db.exec_query(create_group_table)
print("Users and Groups tables created")
