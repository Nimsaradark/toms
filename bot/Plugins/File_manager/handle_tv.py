from Easy_Bot import update , do_task , InlineReplyMarkup
from Easy_Bot.ext import ContextTypes , CallbackContext
from telegram import InputMedia 

from Database import TvDB 
from Config import Reacts , RESULTS_MSG , TV_RESULT
import asyncio
from utils import get_tv_series_poster

@do_task
async def add_tv_command(update: update, context: ContextTypes.DEFAULT_TYPE):
    await update.channel_post.set_reaction(reaction=Reacts.lightning)
    chat = update.effective_chat
    _bot = (await context.bot.get_me()).first_name
    chat_id = chat.id
    chat_title = chat.title
    chat_link = (await context.bot.create_chat_invite_link(chat_id=chat_id,name=_bot)).invite_link
    result = TvDB().add_tv_show(chat_id=chat_id,title=chat_title,link=chat_link)
    print(result)
    await update.channel_post.set_reaction(reaction=Reacts.lightning)
    await update.channel_post.delete()



@do_task
async def remove_tv_command(update: update, context: ContextTypes.DEFAULT_TYPE):
    await update.channel_post.set_reaction(reaction=Reacts.lightning)
    chat = update.effective_chat
    chat_id = chat.id
    result = TvDB().remove_tv_show(chat_id=chat_id)
    print(chat_id,result)
    await update.channel_post.set_reaction(reaction=Reacts.lightning)
    await update.channel_post.delete()


async def GTVX162(update: update, context: CallbackContext):
    asyncio.create_task(handle_tv_request(update,context))

async def handle_tv_request(update: update , context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split(':')
    user_id = int(query_data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer()
    print(query.message.reply_to_message.text)
    tv_list = TvDB().search_tv_shows(title=query.message.reply_to_message.text)
    print(tv_list)
    keyboard = []
    keyboard.append([f"Movie - BC2ML:{update.effective_user.id}","TV Series ✅ - NO:No"])
    if not tv_list:
        await query.answer()
        await query.edit_message_caption(caption="Not found",reply_markup=InlineReplyMarkup(keyboard),parse_mode='HTML')
        return 
    for tv in tv_list:
        keyboard.append([f"{tv.title} - VTX12:{tv.id}:{update.effective_user.id}"])
    keyboard.append([f'🚫 Not Here 🚫 - RDX152:{update.effective_user.id}'])
    reply_markup=InlineReplyMarkup(keyboard)
    try:
        await query.edit_message_caption(caption=RESULTS_MSG,reply_markup=reply_markup,parse_mode='HTML')
    except Exception as e:print(e)


async def GTVX163(update: update ,context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split(':')
    user_id = int(query_data[-1])
    tv_id = int(query_data[1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer("Processing...")
    tv_show = TvDB().get_tv_show(id=tv_id)
    image = get_tv_series_poster(tv_show.title)
    keyboard = InlineReplyMarkup([[f"Download - {tv_show.link}"]])
    text = TV_RESULT.format(title=tv_show.title)
    try:
        media = InputMedia(media=image.poster, media_type='photo',caption=text,parse_mode="HTML")
        await query.edit_message_media(media=media,reply_markup=keyboard)
    except Exception as e:
        print(e)
        await query.edit_message_caption(text,reply_markup=keyboard,parse_mode='HTML')
