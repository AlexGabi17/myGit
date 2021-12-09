import migrations.db_conn as db
import sqlite3
from sqlite3 import Error
path = "migrations/db/myGit.sqlite"
from github import Github
#the get_token() function receive the user_id parameter and it returns the GitHub Token

def get_connection(user_id):
    connection = db.create_connection(path)
    cursor = connection.cursor()
    query = """
        SELECT * FROM users
        WHERE id = """ + str(user_id) + """;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    if rows == []:
        return -1
    #return token
    result_message = rows[0][1]
    
    #test the result/verify if it connects to Github
    try:
        git = Github(rows[0][1])
        #TODO: verify if the credentials are valid

        return git
    except Error as e:
        return -1

