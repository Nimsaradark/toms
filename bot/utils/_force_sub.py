from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import mention_html 
from Config import FORCE_SUB_CHAT , FORCE_SUB_CHAT_LINK , START_IMG , FORCE_SUB_MSG_TEXT , FORCE_SUB_KEYBOARD
from Easy_Bot import InlineReplyMarkup


def force_sub(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if FORCE_SUB_CHAT != None:
            member = (await context.bot.get_chat_member(FORCE_SUB_CHAT, update.effective_user.id)).status
            if member not in ('kicked' , 'left' , 'restricted'):
                await func(update,context)
            else:
                user = mention_html(update.effective_user.id,update.effective_user.first_name)
                await update.effective_message.reply_photo(photo=START_IMG,caption=FORCE_SUB_MSG_TEXT.format(user=user),parse_mode='HTML',reply_markup=InlineReplyMarkup(FORCE_SUB_KEYBOARD(FORCE_SUB_CHAT_LINK)))
        else:
            await func(update,context)
    return wrapper