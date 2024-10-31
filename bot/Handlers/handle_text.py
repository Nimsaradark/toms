from Easy_Bot import update , do_task
from Easy_Bot.ext import ContextTypes
from Plugins.File_manager import handle_movie_requests , add_tv_command , remove_tv_command
from telegram.helpers import mention_html
from Config import GROUPS, TOKEN , INBOX_MSG , BOT_CHAT , INBOX , SUDO_USERS
from Commands import EDCPX52 , EDCPX53 , EDCPX56 , EDCPX57
import asyncio

@do_task
async def message_text_handler(update: update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.delete()
    try:
        if update.effective_chat.id in GROUPS:
            asyncio.create_task(handle_movie_requests(update,context))
    
        if update.message:
            if update.message.reply_to_message and update.effective_message.reply_to_message.from_user.id == int(str(TOKEN.split(':')[0])) and update.effective_message.text:
                text = update.message.reply_to_message.text.split('\n')[-1]
                if text.endswith('Caption'):
                    asyncio.create_task(EDCPX52(update,context))
                if text.endswith('Title'):
                    asyncio.create_task(EDCPX53(update,context))
                if text.startswith('Give me the quality'):
                    asyncio.create_task(EDCPX56(update,context))
                if text.startswith('Give me the File'):
                    asyncio.create_task(EDCPX57(update,context))
                    
        if update.channel_post:
            if update.channel_post.text == '.add':
                asyncio.create_task(add_tv_command(update,context))
            if update.channel_post.text == '.remove':
                asyncio.create_task(remove_tv_command(update,context))
            return
        if update.effective_chat.type == 'private':
            user = update.effective_user
            if user.id in SUDO_USERS:return
            message = update.effective_message
            user_mention = mention_html(user.id,user.first_name)
            text = message.text or message.caption
            msg = INBOX_MSG.format(user=user_mention,user_id=user.id,message=text)
            await context.bot.send_message(chat_id=BOT_CHAT,message_thread_id=INBOX,text=msg,parse_mode='HTML')
    except: pass
