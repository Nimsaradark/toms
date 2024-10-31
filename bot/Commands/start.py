from Easy_Bot import update , InlineReplyMarkup , do_task
from telegram.helpers import mention_html 
from Easy_Bot.ext import ContextTypes , CallbackContext

from Database import check_user_db 
from utils import force_sub
from Config import (
    Reacts , 
    START_IMG , START_MSG_TEXT ,  START_MSG_KEYBOARD , 
    HELP_MSG_TEXT , HELP_MSG_KEYBOARD ,
    WAITING_MSG ,
    MOVIE_STORE
    ) 

__author__ = '@pamod_madubashana'
__command__  = 'start'
__function__ = "start_command"
__description__ = 'use this command to check bot alive'


@force_sub
@check_user_db
@do_task
async def start_command(update: update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.set_reaction(reaction=Reacts.lightning)
    user = mention_html(update.effective_user.id,update.effective_user.first_name)
    if context.args:
        print(context.args)
        message_id = context.args[0].split('_')[-1]
        if 'a' in message_id:
            msgs = message_id.split('a')
            message_id = [i for i in range(int(msgs[0]),int(msgs[-1]) +1)]
        else:
            message_id = [int(message_id)]
        await context.bot.copy_messages(chat_id=update.effective_chat.id,from_chat_id=MOVIE_STORE,message_ids=message_id)
    else:
        CAPTION = START_MSG_TEXT.format(user=user)
        REPLY_MARKUP = InlineReplyMarkup(START_MSG_KEYBOARD(update.effective_user.id))
        await update.message.reply_photo(photo=START_IMG, caption=CAPTION, reply_markup=REPLY_MARKUP, parse_mode='HTML')
    await update.message.delete()


async def help_page(update: update , context: CallbackContext):
    query = update.callback_query
    await query.answer(text=WAITING_MSG)
    user = mention_html(user_id=query.from_user.id,name=query.from_user.first_name)
    CAPTION = HELP_MSG_TEXT.format(user=user)
    REPLY_MARKUP = InlineReplyMarkup(HELP_MSG_KEYBOARD(update.effective_user.id))
    await query.edit_message_caption(caption=CAPTION, reply_markup=REPLY_MARKUP, parse_mode='HTML')
    

