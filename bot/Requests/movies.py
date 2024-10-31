from Easy_Bot import update , do_task , InlineReplyMarkup
from Easy_Bot.ext import ContextTypes , CallbackContext
from utils import get_movies_from_imdb
from Config import WAITING_MSG , BOT_CHAT , REQUEST , SUDO_USERS , DONE_MSG , NOT_RELEASE_MSG , COULDNT_FIND_MSG , REGULATIONS_MSG , WRONG_NAME_MSG , ALEARDY_IN_DB_MSG
import asyncio
from typing import Union

async def FDX152(update: update , context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split(':')
    user_id = int(query_data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    
    search_term = query.message.reply_to_message.text
    movies = await get_movies_from_imdb(search_term)
    if movies:
        movies = sorted(movies, key=lambda x: x['title'] ,reverse=True)
        keyboard = []
        for movie in movies:
            movie_id = movie.getID()
            movie_title = movie.get('title')
            try:
                movie_year = movie.get('year')
                keyboard.append([f"{movie_title} {movie_year} - RQMX16:{movie_id}:{user_id}"])
            except:keyboard.append([f"{movie_title} - RQMX16:{movie_id}:{user_id}"])
        reply_markup = InlineReplyMarkup(keyboard)
        caption="""
<b><i>Here is result found on IMDB</i></b>

<b><i>Select what you want to request</i></b>
"""
        await query.edit_message_caption(caption=caption,reply_markup=reply_markup,parse_mode='HTML')
    else:
        await query.edit_message_caption(caption="<b><i>Not found anything</i></b>",parse_mode='HTML')
        await asyncio.sleep(10)
        await query.message.delete()
        await query.message.reply_to_message.delete()


async def FDX153(update: update , context:Union[ContextTypes.DEFAULT_TYPE ,CallbackContext]):
    query = update.callback_query
    query_data = query.data.split(':')
    user_id = int(query_data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer()

    reply_keyboard = (query.message.reply_markup.inline_keyboard)
    query__data = query.data
    for i in reply_keyboard:
        for j in i:
            if j.callback_data == query__data:
                button = j.text
    caption = "<b><i>Sending Your Request...</i></b>"
    await query.edit_message_caption(caption=caption,reply_markup=None,parse_mode='HTML')
    user = f"<a href='tg://user?id={user_id}'>{query.from_user.first_name}</a>"
    keyboard = [[f"ᴅᴏɴᴇ ✅ - DNX15:D", f"ʀᴇᴊᴇᴄᴛ ❌ - DNX15:R"]]
    await context.bot.send_message(chat_id=BOT_CHAT,message_thread_id=REQUEST,text=f'<i><code>{user_id}</code> : {user}\n\nNew request : {button}</i>',parse_mode="HTML",reply_markup=InlineReplyMarkup(keyboard))
    await context.bot.delete_message(chat_id=query.message.chat_id,message_id=query.message.reply_to_message.message_id)
    await query.message.delete()
    await query.answer('ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴡᴀs sᴇɴᴛ ᴛᴏ ᴀᴅᴍɪɴ',show_alert=True)

async def FDX154(update: update , context:Union[ContextTypes.DEFAULT_TYPE ,CallbackContext]):
    query = update.callback_query
    query_data = query.data.split(':')
    if update.effective_chat.type != 'private': 
        if query.from_user.id not in SUDO_USERS:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
        
    user = query.from_user
    user = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
    message = query.message
    id = int(((message.text).split('\n')[0]).split(':')[0])
    req_text = (message.text.split('\n')[2]).split(':')[1]
    await query.answer()
    data = query_data[1]
    if data == "D":
        text = DONE_MSG.format(req_text=req_text)
        await context.bot.send_message(chat_id=id,text=text,parse_mode='HTML')
        await query.edit_message_text(text=f"<i>{query.message.text}\n\nReply\n─────────────────────\n</i><blockquote><i>{user} : {text}</i></blockquote>",parse_mode='HTML')
    elif data == "R":
        keyboard  = [
            ["ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ʏᴇᴛ - DNX16:0","ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ - DNX16:1","ʀᴇɢᴜʟᴀᴛɪᴏɴs - DNX16:2"],
            ["ᴡʀᴏɴɢ ɴᴀᴍᴇ - DNX16:3","ᴀʟʀᴇᴀᴅʏ ɪɴ ᴛʜᴇʀᴇ - DNX16:4"],
            ["ʙᴀᴄᴋ - DNX16:B"]
            ]
        await query.edit_message_reply_markup(reply_markup=InlineReplyMarkup(keyboard))

async def FDX155(update: update , context):
    query = update.callback_query
    if update.effective_chat.type != 'private': 
        if query.from_user.id not in SUDO_USERS:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    keyboard = [[f"ᴅᴏɴᴇ ✅ - DNX15:D", f"ʀᴇᴊᴇᴄᴛ ❌ - DNX15:R"]]
    await query.edit_message_reply_markup(reply_markup=InlineReplyMarkup(keyboard))

async def FDX156(update: update , context:Union[ContextTypes.DEFAULT_TYPE ,CallbackContext]):
    try:
        query = update.callback_query
        query_data = query.data.split(':')
        if update.effective_chat.type != 'private': 
            if query.from_user.id not in SUDO_USERS:
                await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
                return
        await query.answer()
        data = query_data[1]
        if data == "B":
            asyncio.create_task(FDX155(update,context))
        else:
            final = '❌ Rejected'
            user = query.from_user
            user = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"
            message = query.message
            id = int(((message.text).split('\n')[0]).split(':')[0])
            req_text = (message.text.split('\n')[2]).split(':')[1]
            msg = [NOT_RELEASE_MSG , COULDNT_FIND_MSG , REGULATIONS_MSG , WRONG_NAME_MSG , ALEARDY_IN_DB_MSG]
            data = int(data)
            reply = msg[data].format(req_text=req_text)
            await context.bot.send_message(chat_id=id,text=reply,parse_mode='HTML')
            await query.edit_message_text(text=f"<i>{query.message.text}\n\nReply\n─────────────────────\n<blockquote>{user} : {final}\n{reply}</blockquote></i>",parse_mode='HTML',disable_web_page_preview=True)
    except Exception as e:print("error in sending reply: ",e)
