import logging
import os

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
#def start(update: Update, context: CallbackContext) -> None:
#    """Send a message when the command /start is issued."""
#    user = update.effective_user
#    update.message.reply_markdown_v2(
#        fr'Hi {user.mention_markdown_v2()}\!',
#        reply_markup=ForceReply(selective=True),
#    )


#def help_command(update: Update, context: CallbackContext) -> None:
#    """Send a message when the command /help is issued."""
#    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    # if update.message.text.startswith("https://www.instagram.com/"):
    if update.message.text.startswith("https://coub.com/"):
        update.message.reply_text("Ok! Posted!")
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'db.txt')
        with open(filename, 'w') as writer:
            writer.write(update.message.text)
    else:
        # update.message.reply_text("Bad Instagram video link!")
        update.message.reply_text("Bad COUB video link!")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("BOT_TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    #dispatcher.add_handler(CommandHandler("start", start))
    #dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()