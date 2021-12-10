
#!/usr/bin/env python

"""
myGIt Bot to reply to Telegram messages.

myGit will connect to the github user account and will retrive
relevant informations about the projects he's working at

"""

import logging
import get_connection as github
import migrations.db_conn as db
import sqlite3
from sqlite3 import Error
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


path = "migrations/db/myGit.sqlite"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    """
        The starting message of myGit Bot
    """
    result_start_message = "Hi, " + str(update.message.from_user.first_name) + "! This is myGit 🖥️.\n/help for more information.\nYou should sign in with a personal access token. You can generate it on GitHub.\nhttps://github.com/settings/tokens\nClick on 'Generate new token' then come back and set your token (/set yourToken)"
    update.message.reply_text(result_start_message)
def echo(update, context):
    """Echo the user message"""
    update.message.reply_text(update.message.text)

def help(update, context):
    result_help = "Commands🤖\n\n/start for instructions\n/set yourToken for singing in your github account(❗sign in just in private conversation with the bot❗no one should see your private key)\n/repos retrieves the list of your repositories"
    update.message.reply_text(result_help)

def setUser(update, context):
    token = update.message.text[4:].strip()
    user_id = update.message.from_user.id
    
    connection = db.create_connection(path)

    cursor = connection.cursor()

    if len(token) == 0:
        update.message.reply_text("You should copy the token from GitHub.\nexample: /set yourToken")
        return
    
    if int(update.message.chat_id) < 0:
        update.message.reply_text("You cannot set your token in a group. It's not safe.\nGo private with the bot @@myGit_assistant_bot")
        return 

    try:
       
        #verify if user exist in database, if not, we insert it, else we update the GitHub Token
        verify_query = """
            SELECT * FROM users
            WHERE id = """+ str(user_id) +""";"""
        
        
        cursor.execute(verify_query)
        result = cursor.fetchall()
        if result == []:
            query = """
                INSERT INTO users(id,token)
                VALUES (""" + str(user_id) + """, '""" + str(token) + """');"""
        else:
            query = """
                UPDATE users
                SET TOKEN = '""" + str(token) + """'
                WHERE id = """ + str(user_id) + """;
            """
        cursor.execute(query)
        connection.commit()
        
        update.message.reply_text("Successfully updated your GitHub Access Token")

    except Error as e:
        print(e)
    #insert_username(user_id,username)
    

def get_myRepos(update, context):
    user_id = update.message.from_user.id
    git= github.get_connection(user_id)
    if git == -1:
        update.message.reply_text("You are not registered")
    else:
        index=1
        result="List of all my repositories:\n"
        for repo in git.get_user().get_repos():
            result = result + str(index)+ ". " + repo.name + "\n"
            index = index + 1
        update.message.reply_text(result)

def error(update, context):
    """Log errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    TOKEN =  open('token/token.txt','r').readline().strip()
    print(TOKEN)
    updater = Updater(TOKEN, use_context = True)

    #GET the dispatcher to register handlers
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("help",help))
    dp.add_handler(CommandHandler("set",setUser))
    dp.add_handler(CommandHandler("repos",get_myRepos))
    dp.add_handler(MessageHandler(Filters.text,echo)) 
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()
    


if __name__ == '__main__':
    main()


