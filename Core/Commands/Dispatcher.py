import asyncio
from datetime import datetime
from Core.Util import UtilBot
import traceback

''' To use this, either add on to the ExtraCommands.py file or create your own Python file. Import the DispatcherSingleton
and annotate any function that you wish to be a command with the @DispatcherSingleton.register annotation, and it will
appear in the bot's help menu and be available to use.

For commands that should be hidden, use the @DispatcherSingleton.register_hidden annotation instead, and it won't
appear in the /help menu.

To choose what happens when a command isn't found, register a function with @DispatcherSingleton.register_unknown, and
that function will run whenever the Bot can't find a command that suits what the user entered.'''


class NoCommandFoundError(Exception):
    pass


class CommandDispatcher(object):
    def __init__(self):
        self.commands = {}
        self.hidden_commands = {}
        self.unknown_command = None

    @asyncio.coroutine
    def run(self, bot, event, bot_command_char, *args, **kwds):

        bot_command_char = bot_command_char.strip()  # For cases like "/bot " or " / "

        if args[0] == bot_command_char:  # Either the command char is like "/bot" or the user did "/ ping"
            args = list(args[1:])
        if args[0].startswith(bot_command_char):
            command = args[0][len(bot_command_char):]
        else:
            command = args[0]
        if command[:2] == 'r/':
            command = 'subreddit'
            args = list(args)
            print(args)
            args.insert(1, args[0][3:])
        try:
            func = self.commands[command]
        except KeyError:
            try:
                func = self.hidden_commands[command]
            except KeyError:
                if self.unknown_command:
                    func = self.unknown_command
                else:
                    raise NoCommandFoundError(
                        "Command {} is not registered. Furthermore, no command found to handle unknown commands.".format
                        (command))

        func = asyncio.coroutine(func)

        args = list(args[1:])

        # For help cases.
        if len(args) > 0 and args[0] == '?':
            if func.__doc__:
                bot.send_message_segments(event.conv, UtilBot.text_to_segments(func.__doc__))
                return

        try:
            asyncio.async(func(bot, event, *args, **kwds))
        except Exception as e:
            log = open('log.txt', 'a+')
            log.writelines(str(datetime.now()) + ":\n " + traceback.format_exc() + "\n\n")
            log.close()
            print(traceback.format_exc())

    def register(self, func):
        """Decorator for registering command"""
        self.commands[func.__name__] = func
        return func

    def register_hidden(self, func):
        self.hidden_commands[func.__name__] = func
        return func

    def register_unknown(self, func):
        self.unknown_command = func
        return func

# CommandDispatcher singleton
DispatcherSingleton = CommandDispatcher()

