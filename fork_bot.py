from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging
import requests
import json

#Bot Functions
def startfn(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the FedoraForkFetcher Bot!\n\nList of Commands:\n/help - Gets the Help\n/getforks [REPO_NAME] - Gets the number of forks from a repo\n/listrepos - Lists all the repos in Fedora-Infra")

def helpfn(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="List of Commands:\n/help - Gets the Help\n/getforks [REPO_NAME] - Gets the number of forks from a repo\n/listrepos - Lists all the repos in Fedora-Infra")

def rubbishfn(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unrecognized command! Use /help for a list of commands")

def listforksfn(update, context):
    resp = requests.get("https://api.github.com/orgs/fedora-infra/repos")
    if resp.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An error occured while fetching the Repo list! Please try again in a while")
        return
    repo_json = json.loads(resp.text)
    repo_names = ""
    for i in repo_json:
        repo_names = repo_names+"\n"+i["name"]
    context.bot.send_message(chat_id=update.effective_chat.id, text="List of Repos:\n\n"+repo_names)

def getforksfn(update, context):
    reponame = context.args[0]
    resp = requests.get("https://api.github.com/orgs/fedora-infra/repos")
    if resp.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="An error occured while fetching the Repo list! Please try again in a while")
        return
    repo_json = json.loads(resp.text)
    for i in repo_json:
        if i["name"] == reponame:
            context.bot.send_message(chat_id=update.effective_chat.id, text="The number of forks in the repository "+reponame+" is "+str(i["forks_count"]))
            break 

#Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

#Telegram Initialisation
fork_updater = Updater(token='803028557:AAHnuHOLSs5zBM50_gkD6_PsFMsfacXJKg0', use_context=True)
f_dispatcher = fork_updater.dispatcher

start_handler = CommandHandler('start', startfn)
f_dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', helpfn)
f_dispatcher.add_handler(help_handler)

listrepos_handler = CommandHandler('listrepos', listforksfn)
f_dispatcher.add_handler(listrepos_handler)

getforks_handler = CommandHandler('getforks', getforksfn)
f_dispatcher.add_handler(getforks_handler)

rubbish_handler = MessageHandler(Filters.text, rubbishfn)
f_dispatcher.add_handler(rubbish_handler)

fork_updater.start_polling()
