from uuid import uuid4
import sys
import re
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
API_KEY = sys.argv[1]

XQZS = {0 : "My %s ate my %s.", 1 : "I'm sick.", 2 : "My %s was %s.", 3 : "It's not you, it's me.", 4 : "The %s is %s.", 5 : "I was %s by %s.", 6 : "I %s not %s."}
FILLS = {0 : ["dog", "homework"], 1 : [], 2 : ["mom", "kidnapped"], 3 : [], 4 : ["weather", "horrible"], 5 : ["hit", "a bus"], 6 : ["woke up", "feeling good"]}


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text("Hi! Use '@' to split the phares/words. Example: 'dinossaur@best friend' will become 'My dinossaur ate my best friend'.")


def help(bot, update):
    update.message.reply_text('Help!')


def escape_markdown(text):
    """Helper function to escape telegram markup symbols"""
    escape_chars = '\*_`\['
    return re.sub(r'([%s])' % escape_chars, r'\\\1', text)


def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()
    texts = query.split("@")
    i = 0

    for xqz in XQZS.values():
        try:
            fill = FILLS[i]
            if "%s" in xqz:
                if len(texts) == 2 and texts[0] and texts[1]:
                    output = xqz % (texts[0], texts[1])
                elif len(texts) == 1 and texts[0]:
                    output = xqz % (texts[0], fill[1])
                else:
                    output = xqz % (fill[0], fill[1])
            else:
                output = xqz
            results.append(InlineQueryResultArticle(id=uuid4(),
                                                    title=output,
                                                    input_message_content=InputTextMessageContent(
                                                        output)))
        except Exception as e:
            logger.exception(e)
        i = i + 1

    update.inline_query.answer(results)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()