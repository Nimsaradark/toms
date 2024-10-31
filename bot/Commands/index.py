from Easy_Bot import update , InlineReplyMarkup , do_task , bot
from Easy_Bot.ext import ContextTypes , CallbackContext
from Config import SUDO_USERS , Reacts
from Client import pybot
import math
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.types import Message
import asyncio
from Database import MovieDB
from Classes import MessageData
from utils import movie_parser


__author__ = '@pamod_madubashana'
__command__  = 'index'
__function__ = "index_command"
__description__ = 'use this command to index files'


user_tasks = {}

@do_task
async def index_command(update: update , context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type != 'private':return
    if update.effective_user.id not in SUDO_USERS: return
    if update.effective_message.reply_to_message.document or update.effective_message.reply_to_message.video:
        if update.effective_message.reply_to_message.forward_origin:
            data = update.effective_message.reply_to_message.forward_origin
            chat_id = data.chat.id
            last_message_id = data.message_id

    elif update.effective_message.text:
        data = context.args[0].split('/')
        chat_id = data[-2]
        if chat_id.isnumeric():chat_id = f"-100{chat_id}"
        last_message_id = data[-1]

    else:return
    try:chat = await context.bot.get_chat(chat_id=chat_id)
    except Exception as e:return await update.effective_message.reply_text(f"{str(e)}")
    title = chat.title
    text = f"""
<b>ᴄʜᴀᴛ :</b> <code>{title.capitalize()}</code>
<b>ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs :</b> <code>{last_message_id}</code>

"""
    reply_markup = InlineReplyMarkup([
        [f'Start Index - STIX:{chat_id}:{last_message_id}'],
        ['Cancel - "Close']
    ])
    await update.effective_message.reply_text(text=text,reply_markup=reply_markup,parse_mode='HTML')




async def FG3ZX(upate: update, context: CallbackContext):
    query = upate.callback_query
    if upate.effective_user.id not in SUDO_USERS:return await query.answer()
    data = (query.data).split(':')
    print(data)
    chat_id = int(data[1])
    last_message_id = int(data[-1])

    await pybot.start()
    
    try:
        try:
            await pybot.get_chat(chat_id)
        except ChannelInvalid:
            return await query.answer(
                'This may be a private channel / group. Make me an admin over there to index the files.', 
                show_alert=True
            )
        except (UsernameInvalid, UsernameNotModified): 
            return await query.answer('Invalid Link specified.', show_alert=True)
        
        try:
            k = await pybot.get_messages(chat_id, last_message_id)
        except:
            return await query.answer(
                'Make Sure That I am An Admin In The Channel, if the channel is private', 
                show_alert=True
            )
        
        await query.answer('Starting Index')
    
        task = asyncio.create_task(index_task(upate,chat_id,last_message_id))
        user_tasks[query.from_user.id] = task
    finally:
        await bot('6974189205:AAE91jLrE_e4gES1ea-0vHeSx0Ejzlxu6og').set_message_reaction(chat_id=chat_id,message_id=last_message_id,reaction=Reacts.ok_hand)
        await pybot.stop()

async def index_task(upate: update,chat_id , last_message_id):

    query = upate.callback_query
    text = query.message.text +  """
<b>╭━━━━━━━━━━━━━━━➣</b>
<b>┣⪼ | {progress}</b>
<b>┣⪼ | ᴘᴇʀᴄᴇɴᴛᴀɢᴇ : <code>{percentage} %</code></b>
<b>┣⪼ | ᴇxᴄʟᴜᴅᴇᴅ : <code>{add}</code></b>
<b>┣⪼ | ᴇxᴄᴇᴘᴛᴇᴅ : <code>{exc}</code></b>
<b>┣⪼ | ᴛᴏᴛᴀʟ sɪᴢᴇ : <code>{total_size} GB</code></b>
<b>╰━━━━━━━━━━━━━━━➣</b>"""

    done = query.message.text +  """
<b>╭━━━━━━━━━━━━━━━➣</b>
<b>┣⪼ | ᴇxᴄʟᴜᴅᴇᴅ : <code>{add}</code></b>
<b>┣⪼ | ᴇxᴄᴇᴘᴛᴇᴅ : <code>{exc}</code></b>
<b>┣⪼ | ᴛᴏᴛᴀʟ sɪᴢᴇ : <code>{total_size} GB</code></b>
<b>╰━━━━━━━━━━━━━━━➣</b>"""
    
    reply_markup = InlineReplyMarkup([
        ['Cancel - "Close']
    ])            
    current = 0
    total_size = 0
    add = 0
    exc = 0
    while True:
        new_diff = min(10, last_message_id - current)
        if new_diff <= 0:break
        readed_msg = await pybot.get_messages(chat_id, list(range(current, current+new_diff+1)))
        for msg in readed_msg:
            if msg.document or msg.video:
                try:
                    file_name = msg.caption
                    movie_title = movie_parser.title(file_name)
                    movie_category = movie_parser.category_title(file_name)
                    save_title = MovieDB().is_in_saved_movies(movie_title)
                    in_database = MovieDB().is_file_in_saved_movies(movie_title.lower(),movie_category)
                    if not save_title:
                        MovieDB().add_title_to_db(message_id=msg.id,title=movie_title)
                    if not in_database:
                        MovieDB().add_movie_to_db(message_id=msg.id,title=movie_title,quality=movie_category,file_size=round((msg.document.file_size or msg.video.file_size)/1024/1024,2) )

                    try:total_size = total_size + round((msg.document.file_size or msg.video.file_size)/1024/1024,2) 
                    except:pass

                    add = add + 1
                except:
                    exc = exc + 1
                    
                
            else:
                exc = exc + 1

            current += 1
            progress_fill = "⬢"
            progress_pending = "⬡"
            if msg.id % 50 == 0 or current ==1:
                percentage = round(((msg.id / last_message_id)*100),2)
                
                progress = f"""{"".join([progress_fill for i in range(math.floor(percentage / 7))])}{"".join([progress_pending for i in range(14 - math.floor(percentage / 7))])} """
                await query.edit_message_text(
                    str(text).format(
                        percentage=percentage,
                        progress=progress,
                        add=f"{add}/{last_message_id}",
                        exc = f"{exc}/{last_message_id}",
                        total_size=round((total_size/1024),2),
                        ),
                    reply_markup=reply_markup,parse_mode='HTML')
            if msg.id == last_message_id:
                await query.edit_message_text(text=str(done).format(add=f"{add}/{last_message_id}",exc = f"{exc}/{last_message_id}",total_size=round((total_size/1024),2)),parse_mode='HTML')
    


   

async def cancel_task(update: update, context: CallbackContext):
    query = update.callback_query
    button = query.data
    data = button.split(":")
    user_id =int(data[-1])
    if user_id != query.from_user.id:
        await query.answer("This is not for you",show_alert=True)
        return
    if user_id in user_tasks:
        task = user_tasks[user_id]
        try:
            task.cancel()
            await query.answer("task cancelled.",show_alert=True)
            await query.message.delete()
            await context.bot.delete_message(chat_id=query.message.chat.id,message_id=query.message.reply_to_message.message_id)
        except Exception as e:
            await query.answer(e,show_alert=True)
    else:
        await query.answer("No running task to cancel.",show_alert=True)
