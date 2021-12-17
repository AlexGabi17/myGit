from migrations.db_conn import Database
from github import Github
from github import GithubException
#the get_token() function receive the user_id parameter and it returns the GitHub Token

def get_connection(db: Database, user_id: int):
    rows = db.select('users', user_id)

    if rows == []:
        return -1
    
    # test the result/verify if it connects to Github
    try:
        git = Github(rows[0][1])
        git.get_repo(1)
        return git
    except GithubException as e:
        return -1


