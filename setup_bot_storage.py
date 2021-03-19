from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.update import Update
from app.storage.telegram.bot import updater

# Run this file with bot in channel as admin to get channel_id use in CID enviroment variable


def cid(update: Update, context: CallbackContext):
    id = update.channel_post.chat.id
    text = update.channel_post.text

    if text == 'cid':
        update.channel_post.reply_text(id)


if __name__ == '__main__':
    print('Add your bot with privacy mode disabled as admin in your channel')
    print('Text in your channel cid to get channel id and setup CID enviroment variable')

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, cid))

    updater.start_polling()
    updater.idle()
