from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from app.storage.telegram.bot import updater


# Run this file with bot in channel as admin to get channel_id use in CID enviroment variable
async def cid(update: Update, _: ContextTypes.DEFAULT_TYPE):
    chat_id = update.channel_post.chat.id
    print(f"CID: {chat_id}")
    text = update.channel_post.text

    if text == "cid":
        await update.channel_post.reply_text(str(chat_id))


def main():
    print("Add your bot with privacy mode disabled as admin in your channel")
    print(
        "Text in your channel `cid` to get channel id and setup CID enviroment variable"
    )

    updater.add_handler(MessageHandler(filters.TEXT, cid))

    updater.run_polling()


if __name__ == "__main__":
    main()
