import db_conn as db
conn = db.create_connection("db/myGit.sqlite")
create_user_table = """
    CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY,
    token TEXT NOT NULL
    )
"""
db.execute_query(conn, create_user_table)
