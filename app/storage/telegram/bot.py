from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram import Update

from app.core.config import TOKEN


def cid(update: Update, context: CallbackContext):
    id = update.channel_post.chat.id
    text = update.channel_post.text

    if text == 'cid':
        update.channel_post.reply_text(id)


updater = Updater(TOKEN, use_context=True)

bot = updater.bot
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.text, cid))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
