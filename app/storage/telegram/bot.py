from telegram.ext import Updater, CallbackContext, MessageHandler, Filters
from telegram import Update

from app.core.config import TOKEN


updater = Updater(TOKEN, use_context=True)
bot = updater.bot
