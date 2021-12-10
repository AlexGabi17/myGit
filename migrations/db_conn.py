import sqlite3
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        #print("Connection to database succesful")
    except Error as e:
        print(f"The error '{e}' occured")
        raise Error(e)
    return connection

def execute_query(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed succesfully")
    except Error as e:
        print(f"The error '{e}' occured")

def select_query(connection,query):
    cursor = connection.cursor()
    cursor.execute(query)
    
    rows = cursor.fetchall()

    for row in rows:
        print(row[1])
