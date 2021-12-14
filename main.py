
#!/usr/bin/env python3

"""
myGIt Bot to reply to Telegram messages.

myGit will connect to the github user account and will retrive
relevant informations about the projects he's working at

"""

import logging
import get_connection as github
from migrations.db_conn import Database
from sqlite3 import Error
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram.update import Update

path = "migrations/db/myGit.sqlite"
db = Database(path)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """
        The starting message of myGit Bot
    """
    result_start_message = "Hi, " + str(update.message.from_user.first_name) + "! This is myGit 🖥️.\n/help for more information.\nYou should sign in with a personal access token. You can generate it on GitHub.\nhttps://github.com/settings/tokens\nClick on 'Generate new token' then come back and set your token (/set yourToken)"
    update.message.reply_text(result_start_message)

def echo(update: Update, context: CallbackContext):
    """Echo the user message"""
    update.message.reply_text(update.message.text)

def help(update: Update, context: CallbackContext):
    result_help = "Commands🤖\n\n/start for instructions\n/set yourToken for singing in your github account(❗sign in just in private conversation with the bot❗no one should see your private key)\n/repos retrieves the list of your repositories\n\nFor repositories:\n\n/setrepo yourRepository (i.e. username/Repository_name)"
    update.message.reply_text(result_help)

def setUser(update: Update, context: CallbackContext):
    token = update.message.text[4:].strip()
    user_id = update.message.from_user.id
    
    if int(update.message.chat_id) < 0:
        update.message.reply_text("You cannot set your token in a group. It's not safe.\nGo private with the bot @myGit_assistant_bot")
        return

   
    if len(token) == 0:
        update.message.reply_text("You should copy the token from GitHub.\nexample: /set yourToken")
        return
    
    try:
        #verify if user exist in database, if not, we insert it, else we update the GitHub Token
        result = db.select('users', user_id)

        if result == []:
            db.insert('users',{'id': str(user_id), 'token': token})   
        else:
            db.update_user_token({'id': str(user_id), 'token': token})
        
        update.message.reply_text("Successfully updated your GitHub Access Token")

    except Error as e:
        print('Custom Error: ', e)
    #insert_username(user_id,username)
    

def get_myRepos(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    git = github.get_connection(db, user_id)
    if git == -1:
        update.message.reply_text("You are not registered if you are new. Or your Github token is not valid( it's wrong or expired ).")
    else:
        index=1
        result="List of all my repositories:\n"
        for repo in git.get_user().get_repos():
            result = result + str(index)+ ". " + repo.name + "\n"
            index = index + 1
        update.message.reply_text(result)

def setRepoInChat(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    group_id = int(update.message.chat_id)
    repo_name = update.message.text[8:].strip()

    git = github.get_connection(db, user_id)
    
    if group_id > 0:
        update.message.reply_text("Go on your group and set the Group's repository.")
        return
    elif len(repo_name) == 0:
        update.message.reply_text("You have to specify a repo name(i.e. username/myfirstrepo)")
    else:
        #verify if the repo received as param does exist
        if github.verify_repo(git, repo_name) == -1:
            update.message.reply_text("This repository doesn't exist.")
            return

        try:
            result = db.select('groups', group_id)

            if result == []:
                db.insert('groups',{'id': str(group_id), 'repo': repo_name})   
            else:
                db.update_group_repo({'id': str(group_id), 'repo': repo_name})
            
            update.message.reply_text("Successfully set the repository.☑️")
        except Error as e:
            print('Custom Error: ', e)


def error(update: Update, context: CallbackContext):
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
    dp.add_handler(CommandHandler("setrepo",setRepoInChat))
    dp.add_handler(MessageHandler(Filters.text,echo)) 
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()
    


if __name__ == '__main__':
    main()


