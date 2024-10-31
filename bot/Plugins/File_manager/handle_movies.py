from Easy_Bot import update , InlineReplyMarkup 
from telegram import InputMedia 
from telegram.helpers import mention_html
from Easy_Bot.ext import ContextTypes , CallbackContext
from utils import movie_parser
from Database import MovieDB
from Config import Reacts , WAITING_MSG , NO_RESULTS_MSG , RESULTS_MSG , SELECT_QUALITY , HERE_ARE_FILES , MOVIE_DETAILS_MSG_TEXT , SEARCHING_IMGS
from utils import MoviesDetails , delete_scheduler
from typing import Union
import asyncio
import random

reacts = ['👌', '❤️', '⚡', '🔥', '🎉', '😇', '😍']

async def handle_movie_requests(update: update , context: ContextTypes.DEFAULT_TYPE):
    if update.callback_query:
        query = update.effective_message.reply_to_message.text  
    else:    
        try:await update.effective_message.set_reaction(reaction=random.choice(reacts))
        except:pass
        m = await update.effective_message.reply_photo(photo=random.choice(SEARCHING_IMGS),caption=WAITING_MSG,parse_mode='HTML',quote=True)
        await delete_scheduler(context=context,chat_id=update.effective_chat.id, message_id=update.effective_message.message_id,time=900)
        await delete_scheduler(context=context,chat_id=update.effective_chat.id, message_id=m.message_id,time=900)
        query = update.effective_message.text
    user = mention_html(update.effective_user.id,update.effective_user.first_name)
    results = MovieDB().search_movies(query)
    keyboard = []
    keyboard.append(["Movie✅ - NO:No",f"TV Series - TCX51:{update.effective_user.id}"])
    if results:
        for result in results:
            keyboard.append([f"{movie_parser.upper_title(result.title)} - MVFX2:{result.id}:{update.effective_user.id}"])
        text = RESULTS_MSG.format(search_query=query.title(),user=user)
    else:        
        text = NO_RESULTS_MSG.format(search_query=query)
    keyboard.append([f'🚫 Not Here 🚫 - RDX152:{update.effective_user.id}'])
    reply_markup=InlineReplyMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.edit_message_caption(caption=text,reply_markup=reply_markup,parse_mode='HTML')
    else:
        await m.edit_caption(caption=text,reply_markup=reply_markup,parse_mode='HTML')

async def B2MLX1(update: update, context: CallbackContext):
    asyncio.create_task(handle_movie_requests(update,context))

async def MSX34(update: update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split(':')
    user_id = int(query_data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer()
    movie_id = int(query_data[-2])
    movie = MovieDB().get_movie(movie_id)
    keyboard = []
    for quality in movie['quality']:
        keyboard.append([f"{quality} - GSX21:{movie_id}:{quality}:{update.effective_user.id}"])
    keyboard.append([f"<< Back - BC2ML:{update.effective_user.id}"])
    title = movie['title']

    await query.edit_message_caption(caption=SELECT_QUALITY,reply_markup=InlineReplyMarkup(keyboard),parse_mode='HTML')


async def GSX34(update: update, context: CallbackContext):
    query = update.callback_query
    query_data = query.data.split(':')
    user_id = int(query_data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer()
    movie_id = int(query_data[1])
    quality = query_data[2]
    movie = MovieDB().get_movie(movie_id)

    keyboard = []
    for exten in movie['quality'][quality]:
        data = str(movie['quality'][quality][exten]).split('-') 
        exten = str(exten).replace('Blu-ray','BluRay')
        message_id = data[0]
        file_size = f"{data[-1]} MB" if float(data[-1]) <= 1023 else f"{round(float(data[-1])/1024 , 2)} GB"
        if ',' in message_id:
            message_id = message_id.split(',')[0] + "a" + message_id.split(',')[-1]
        keyboard.append([f"{str(exten).replace('-',' ')} -{file_size} - SDX63:{movie_id}:{message_id}:{update.effective_user.id}"])

    keyboard.append([f"<< Back - MVFX2:{movie_id}:{update.effective_user.id}"])

    title = movie['title']
    await query.edit_message_caption(caption=HERE_ARE_FILES.format(quality=quality),reply_markup=InlineReplyMarkup(keyboard),parse_mode='HTML')

async def THDX23(update: update , context: Union[CallbackContext,ContextTypes.DEFAULT_TYPE]):
    query = update.callback_query
    data = query.data.split(':')
    user_id = int(data[-1])
    if update.effective_chat.type != 'private': 
        if user_id != query.from_user.id:
            await query.answer("ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ꜰᴏʀ ʏᴏᴜ",show_alert=True)
            return
    await query.answer("Processing...")
    bot = await context.bot.get_me()
    username = bot.username
    message_id = data[-2]
    movie_id = int(data[-3])
    movie = MovieDB().get_movie(movie_id)
    title = movie_parser.upper_title(movie['title'])
    mdetails = MoviesDetails(movie_name=title,source='tmdb').get_details()

    quality = str(query.message.caption)
    for d in HERE_ARE_FILES.replace('<b>','').replace('</b>','').replace('<i>','').replace('</i>','').split('{quality}'):
        quality = quality.replace(d,'')
    reply_keyboard = (query.message.reply_markup.inline_keyboard)
    query_data = query.data
    for i in reply_keyboard:
        for j in i:
            if j.callback_data == query_data:
                file = j.text.split("-")[0]
    # return
    # released=movieDetails.released
    # languages=movieDetails.languages
    # year=movieDetails.year
    # genres=movieDetails.genres
    # image=movieDetails.image
    # rating=movieDetails.rating
    # votes=movieDetails.votes

    text = MOVIE_DETAILS_MSG_TEXT.format(
        released = mdetails.released,
        languages = mdetails.languages,
        genres = mdetails.genres,
        rating = mdetails.rating,
        votes = mdetails.votes,
        file_name = (title + "()" +  quality + " " + file)
        # year=mdetails.year,

    )

    link = f"https://t.me/{username}?start=movie_{message_id}"
    reply_markup = InlineReplyMarkup([
        [f'🔰 ᴅᴏᴡɴʟᴏᴀᴅ 🔰 - {link}']
    ])
    try:
        media = InputMedia(media=mdetails.image, media_type='photo',caption=text,parse_mode="HTML")
        await query.edit_message_media(media=media,reply_markup=reply_markup)
    except:
        await query.edit_message_caption(caption=text,parse_mode='HTML',reply_markup=reply_markup)


async def Manage_movie_database(update: update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_message.document:return
    document = update.effective_message.document
    file_name = update.effective_message.caption
    file_size = int(document.file_size/1024/1024)
    file_unique_id = document.file_unique_id
    message = update.effective_message
    message_id = update.effective_message.id
    await message.set_reaction(reaction=Reacts.moai)
    try:

        movie_title = movie_parser.title(file_name)
        movie_category = movie_parser.category_title(file_name)
        movie_file_name = movie_parser.cleared_file_name(file_name)
        save_title = MovieDB().is_in_saved_movies(movie_title)
        in_database = MovieDB().is_file_in_saved_movies(movie_title.lower(),movie_category)
        print(movie_category)
        if not save_title:
            try:
                result = MovieDB().add_title_to_db(message_id=message_id,title=movie_title)
    
            except Exception as e:print(e)
        
        try:
            result = MovieDB().add_movie_to_db(message_id=message_id,title=movie_title,quality=movie_category,file_size=file_size,unique_id=file_unique_id)
            await message.set_reaction(reaction=Reacts.ok_hand)
        except Exception as e:print(e)

    except Exception as e:
        await message.set_reaction(reaction=Reacts.broken_heart)
        await message.edit_caption(caption=f'<i>{movie_file_name}</i>\n\n<code>Error : {str(e)}</code>',parse_mode='HTML')

