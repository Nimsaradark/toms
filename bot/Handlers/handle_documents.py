from Easy_Bot import update , do_task
from Easy_Bot.ext import ContextTypes
from Config import  MOVIE_STORE
from Plugins.File_manager import Manage_movie_database
import asyncio

@do_task
async def message_document_handler(update: update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if chat_id == MOVIE_STORE:
        asyncio.create_task(Manage_movie_database(update,context))
    
