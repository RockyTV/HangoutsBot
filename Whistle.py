# Add new /<command name> based commands in command.py
# Add any other new commands in handlers.py handle function.


# Useless function? Maybe...
from hangupsbot import HangupsBot


def start():
    bot = HangupsBot("cookies.txt", "config.json")
    bot.run()


start()