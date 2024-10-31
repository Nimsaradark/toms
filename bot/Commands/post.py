from Easy_Bot import update , InlineReplyMarkup , do_task 
from Easy_Bot.ext import ContextTypes , CallbackContext
from typing import Union
from Database import MovieDB 
from utils import MoviesDetails
from Config import Reacts , BOT_TEXT ,SUDO_USERS , CHANNEL_POST_MSG , MAIN_CHANNEL , DOWNLOAD_BUTTON, ST_LOAD
    

__author__ = '@pamod_madubashana'
__command__  = 'post'
__function__ = "post_command"
__description__ = 'use this command to edit data in database'

@do_task
async def post_command(update: update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SUDO_USERS:return await update.message.delete()
    await update.message.set_reaction(reaction=Reacts.lightning)
    query = ' '.join((update.effective_message.text).split(' ')[1:])
    if query != '':
        m = await update.message.reply_text(text=BOT_TEXT,parse_mode='HTML')
        mdetails = MoviesDetails(movie_name=query,source='imdb').get_details()
        text = CHANNEL_POST_MSG.format(
            title = mdetails.name,
            released = mdetails.released,
            languages = mdetails.languages,
            genres = mdetails.genres,
            rating = mdetails.rating,
            votes = mdetails.votes,
            # year=mdetails.year,
        )
        keyboard = [['send - SDTX15:sudo']]
        await update.message.reply_photo(photo=mdetails.image,caption=text,parse_mode='HTML',reply_markup=InlineReplyMarkup(keyboard),quote=True)
        await m.delete()
    else:
        await update.message.delete()


async def SDTX12(update: update, context: Union[ContextTypes.DEFAULT_TYPE, CallbackContext] ):
    query = update.callback_query
    reply_markup=InlineReplyMarkup(DOWNLOAD_BUTTON())
    await context.bot.copy_message(from_chat_id=update.effective_chat.id,chat_id=MAIN_CHANNEL,message_id=query.message.message_id,reply_markup=reply_markup)
    await context.bot.send_sticker(chat_id=-1002330710763, sticker=ST_LOAD)
    await query.answer("Done")
    await query.message.reply_to_message.delete()
    await query.delete_message()
