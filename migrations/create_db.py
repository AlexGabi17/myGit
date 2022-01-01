from db_conn import Database

db = Database("migrations/db/myGit.sqlite")
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
create_todo_table = """
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER,
        repo INTEGER,
        todo TEXT NOT NULL,
        due_date DATE DEFAULT NULL,
        created_at DATE DEFAULT (date('now')),
        completed BOOL DEFAULT FALSE,
        FOREIGN KEY(id) REFERENCES users(id)
        FOREIGN KEY(repo) REFERENCES groups(id)
    )
"""
db.exec_query(create_todo_table)
print("Users, Groups and Todos tables created")
