from telegram.ext import Application

from app.core.config import TOKEN

updater = Application.builder().token(TOKEN).build()
bot = updater.bot
