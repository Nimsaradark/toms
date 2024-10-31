from Easy_Bot import update , InlineReplyMarkup , do_task 
from telegram import ForceReply 
from telegram.helpers import mention_html 
from Easy_Bot.ext import ContextTypes , CallbackContext
from typing import Union
from Database import MovieDB 
from utils import force_sub , movie_parser
from Config import (
    Reacts , 
    START_IMG , START_MSG_TEXT, 
    FIND_BUTTONS,EDIT_DB_BUTTONS,
    DELETE_BUTTONS , 
    BOT_TEXT ,
    MOVIE_STORE,
    SUDO_USERS
    ) 

__author__ = '@pamod_madubashana'
__command__  = 'find'
__function__ = "find_command"
__description__ = 'use this command to edit data in database'


FIND_TEXT = """
◉ <b>ID  :</b> <code>{id}</code>
◉ <b>unique_id :</b> <code>{unique_id}</code>

┌ <b>Title :</b> <code>{title}</code>
├ <b>Quality :</b> <code>{quality}</code>
├ <b>File Size :</b> <code>{file_size}</code>
├ <b>FIle :</b> <code>{category}</code>
├ <b>File ID :</b> <code>{file_id}</code>
└ <b>Caption :</b> <code>{caption}</code>
"""

@do_task
async def find_command(update: update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in SUDO_USERS:return
    await update.message.set_reaction(reaction=Reacts.lightning)
    m = await update.message.reply_text(text=BOT_TEXT,parse_mode='HTML')
    
    if update.message.reply_to_message:
        message = update.message.reply_to_message
        UID = message.document.file_unique_id
        save = dict(MovieDB().find_file(UID)) if MovieDB().find_file(UID) else None
        
        async def check_file_unique_id(save):
            id = save.get('movie_id', None) 
            if id:
                file_id = save['file_id']
                quality = save['quality']
                exten = save['exten']
                movie = MovieDB().get_movie(id=int(id))

                title = movie['title']
                caption = message.caption
                file_size = round((int(message.document.file_size)/1024/1024),2)
                file_size = f"{file_size} MB" if file_size <= 1023 else f"{round((file_size/1024),2)} GB"
                reply_markup=InlineReplyMarkup(FIND_BUTTONS())
                await m.edit_text(text=FIND_TEXT.format(id=id,unique_id=UID,title=title,quality=quality,caption=caption,category=exten,file_id=file_id,file_size=file_size),parse_mode='HTML',reply_markup=reply_markup)
                
            else:
                MovieDB().delete_unique_id(UID)
                await check_file_caption(message)
           
        async def check_file_caption(message):
            title = movie_parser.title(message.caption).lower()
            category = movie_parser.category_title(message.caption)
            data = MovieDB().is_file_in_saved_movies(movie_title=title,category=category,get_details=True)
            if data:
                print(data)
                id = data.get('_id')
                category_info = category.split('-')
                quality = category_info[0]
                category = '-'.join(category_info[1:])
                file_id = str(data.get('quality').get(quality).get(category)).split('-')[0]
                caption = message.caption
                file_size = round((int(message.document.file_size)/1024/1024),2)
                file_size = f"{file_size} MB" if file_size <= 1023 else f"{round((file_size/1024),2)} GB"
                reply_markup=InlineReplyMarkup(FIND_BUTTONS())
                await m.edit_text(text=FIND_TEXT.format(id=id,unique_id=UID,title=title,quality=quality,caption=caption,category=category,file_id=file_id,file_size=file_size),parse_mode='HTML',reply_markup=reply_markup)
                MovieDB().add_unique_id(unique_id=UID,movie_id=id,message_id=file_id,quality=quality,exten=category)
                return
        if save:
            await check_file_unique_id(save)
            return
        else:
            await check_file_caption(message)
            return
        await m.edit_text(text='<code>Not found</code>',parse_mode='HTML')

        

async def EDCX12(update: update, context: Union[ContextTypes.DEFAULT_TYPE, CallbackContext] ):
    query = update.callback_query
    file_id = int(str(query.message.text).split('\n')[-2].replace('├ File ID :',''))
    movie_id = int(str(query.message.text).split('\n')[0].replace('◉ ID  :',''))
    reply_markup=InlineReplyMarkup(EDIT_DB_BUTTONS(file_id,movie_id))
    await query.edit_message_reply_markup(reply_markup=reply_markup)

async def EDCX11(update: update, context: Union[ContextTypes.DEFAULT_TYPE, CallbackContext]):
    await update.callback_query.edit_message_reply_markup(InlineReplyMarkup(FIND_BUTTONS()))

async def EDCPX52(update: update, context: Union[ContextTypes.DEFAULT_TYPE,CallbackContext]):
    if update.callback_query:
        query = update.callback_query
        query_data = query.data.split(':')
        file_id = query_data[1]
        if file_id != 'sudo':
            await query.answer()
            caption = str(query.message.text).split('\n')[-1].replace('└ Caption :','')
            await context.bot.send_message(
                text=f'{file_id}\n{query.message.message_id}\nGive me the text for Caption',
                reply_markup=ForceReply(input_field_placeholder=caption),
                reply_to_message_id=query.message.message_id,
                chat_id=update.effective_chat.id,
            )
        else:
            await query.answer()
            text = str(query.message.reply_to_message.text).split('\n')
            id , unique_id, _ , title , quality , file_size , category , file_id , _  = [d.split(" : ")[-1] for d in text]
            caption = query.message.text.split('\n')[-1]
            await context.bot.edit_message_text(chat_id=update.effective_chat.id,message_id=query.message.reply_to_message.message_id,text=FIND_TEXT.format(id=id,unique_id=unique_id,title=title,quality=quality,caption=caption,category=category,file_id=file_id,file_size=file_size),reply_markup=InlineReplyMarkup(FIND_BUTTONS()),parse_mode='HTML')
            await context.bot.edit_message_caption(chat_id=MOVIE_STORE,message_id=int(file_id),caption=f"<b><i>{caption}</i></b>",parse_mode='HTML')
            await update.effective_message.delete()

    else:
        query = update.effective_message.text
        messages = update.effective_message.reply_to_message.text.split('\n')
        file_id = int(messages[0])
        message_id = int(messages[1])
        message = update.effective_message.reply_to_message
        t1 = update.effective_message.message_id
        t2 =  message.message_id
        await context.bot.delete_message(chat_id=update.effective_chat.id,message_id=t1)

        reply_markup = InlineReplyMarkup([
            ['Confirm - ECPX1:sudo'],
            ['Cancel - Close']
        ])
        await message.delete()
        await update.message.reply_text(text=f'Confirm?\n<code>{query}</code>',reply_markup=reply_markup,reply_to_message_id=message_id,parse_mode='HTML')
        

async def EDCPX53(update: update, context: Union[ContextTypes.DEFAULT_TYPE,CallbackContext]):
    if update.callback_query:
        query = update.callback_query
        query_data = query.data.split(':')
        file_id = query_data[1]
        if file_id != 'sudo':
            await query.answer()
            title = str(query.message.text).split('\n')[3].replace('┌ Title :','')
            await context.bot.send_message(
                text=f'{file_id}\n{query.message.message_id}\nGive me the text for Title',
                reply_markup=ForceReply(input_field_placeholder=title),
                reply_to_message_id=query.message.message_id,
                chat_id=update.effective_chat.id,
            )
        else:
            await query.answer()
            text = str(query.message.reply_to_message.text).split('\n')
            id , unique_id, _ , _ , quality , file_size , category , file_id , caption  = [d.split(" : ")[-1] for d in text]
            title = query.message.text.split('\n')[-1]
            result = MovieDB().edit_movie_title(id=int(id),title=title)
            MovieDB().update_unique_id(unique_id=unique_id,movie_id=int(id),message_id=int(file_id),quality=quality,exten=category)
            await context.bot.edit_message_text(chat_id=update.effective_chat.id,message_id=query.message.reply_to_message.message_id,text=FIND_TEXT.format(id=id,unique_id=unique_id,title=title,quality=quality,caption=caption,category=category,file_id=file_id,file_size=file_size),reply_markup=InlineReplyMarkup(FIND_BUTTONS()),parse_mode='HTML')
            await update.effective_message.delete()

    else:
        query = update.effective_message.text
        messages = update.effective_message.reply_to_message.text.split('\n')
        file_id = int(messages[0])
        message_id = int(messages[1])
        message = update.effective_message.reply_to_message
        t1 = update.effective_message.message_id
        t2 =  message.message_id
        await context.bot.delete_message(chat_id=update.effective_chat.id,message_id=t1)

        reply_markup = InlineReplyMarkup([
            ['Confirm - ETPX1:sudo'],
            ['Cancel - Close']
        ])
        await message.delete()
        await update.message.reply_text(text=f'Confirm?\n<code>{query}</code>',reply_markup=reply_markup,reply_to_message_id=message_id,parse_mode='HTML')


async def EDCPX54(update: update, context: CallbackContext):
    query = update.callback_query
    await query.answer("Confirm to delete file from Database")
    messages = update.effective_message.text.split('\n')
    movie_id = int((messages[0]).split(':')[-1])
    file_id = int(messages[-2].split(':')[-1])
    reply_markup = InlineReplyMarkup(DELETE_BUTTONS(file_id,movie_id))
    await query.edit_message_reply_markup(reply_markup)


async def EDCPX55(update: update, context: Union[ContextTypes.DEFAULT_TYPE,CallbackContext]):
    query = update.callback_query
    query_data = query.data.split(':')
    file_id = int(query_data[1])
    movie_id = int(query_data[-1])
    delete = MovieDB().delete_file(file_id=file_id,Movie_id=movie_id)
    if delete:
        await query.answer("File deleted")
        await context.bot.delete_message(chat_id=MOVIE_STORE,message_id=file_id)
        try:context.bot.delete_message(chat_id=update.effective_chat.id,message_id=update.effective_message.reply_to_message.message_id)
        except:pass
        await query.delete_message()
    else:
        await query.answer("Something went wrong")
        await query.edit_message_reply_markup(InlineReplyMarkup(FIND_BUTTONS()))
    


async def EDCPX56(update: update , context: Union[CallbackContext , ContextTypes.DEFAULT_TYPE]):
    if update.callback_query:
        query = update.callback_query
        query_data = query.data.split(':')
        method = query_data[1]
        
    
        if method == 'S':
            await query.answer()
            file_id = int(query_data[2])
            message = update.effective_message.text.split('\n')
            quality = message[4].replace('├ Quality :','')
            await context.bot.send_message(
                    text=f'{file_id}\n{query.message.message_id}\nGive me the quality for replace {quality}',
                    reply_markup=ForceReply(input_field_placeholder=quality),
                    reply_to_message_id=query.message.message_id,
                    chat_id=update.effective_chat.id,
                )
        elif method == 'C':
            await query.answer()
            text = str(query.message.reply_to_message.text).split('\n')
            caption = text[-1]
            id , unique_id, _ , title , quality , file_size , category , file_id , _  = [d.split(" : ")[-1] for d in text]
            qmsg = str(query.message.text).split(' ->> ')
            current_quality = qmsg[0]
            new_quality = qmsg[1]
            quality = new_quality
            result = MovieDB().edit_quality(id=int(id),file_id=int(file_id),current_quality=current_quality,new_quality=new_quality)
            MovieDB().update_unique_id(unique_id=unique_id,movie_id=int(id),message_id=int(file_id),quality=quality,exten=category)
            await update.effective_message.delete()
            await context.bot.edit_message_text(chat_id=update.effective_chat.id,message_id=query.message.reply_to_message.message_id,text=FIND_TEXT.format(id=id,title=title,quality=quality,caption=caption,category=category,file_id=file_id,file_size=file_size),reply_markup=InlineReplyMarkup(FIND_BUTTONS()),parse_mode='HTML')

    else:
        await update.message.delete()
        await update.message.reply_to_message.delete()
        query = update.effective_message.text
        message = update.effective_message.reply_to_message.text.split('\n')
        file_id = int(message[0])
        bot_msg_id = int(message[1])
        current_quality = message[2].split(' ')[-1]
        new_quality = query
        text = f"{current_quality} ->> {new_quality}"
        keyboard = [[f'Confirm - EQPX1:C:sudo'],['Cancel - Close']]
        await context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=InlineReplyMarkup(keyboard),reply_to_message_id=bot_msg_id)
        



async def EDCPX57(update: update , context: Union[CallbackContext , ContextTypes.DEFAULT_TYPE]):
    if update.callback_query:
        query = update.callback_query
        query_data = query.data.split(':')
        method = query_data[1]


        if method == 'S':
            await query.answer()
            file_id = int(query_data[2])
            message = update.effective_message.text.split('\n')
            file = message[6].replace('├ FIle :','')
            await context.bot.send_message(
                    text=f'{file_id}\n{query.message.message_id}\nGive me the File for replace {file}',
                    reply_markup=ForceReply(input_field_placeholder=file),
                    reply_to_message_id=query.message.message_id,
                    chat_id=update.effective_chat.id,
                )
        elif method == 'C':
            try:
                await query.answer()
                await update.effective_message.delete()
                text = str(query.message.reply_to_message.text).split('\n')
                caption = text[-1]
                id , unique_id, _ , title , quality , file_size , category , file_id , _  = [d.split(" : ")[-1] for d in text]
                qmsg = str(query.message.text).split(' ->> ')
                current_file = qmsg[0]
                new_file = qmsg[1]
                file = new_file
                result = MovieDB().edit_file_exten(id=int(id),quality=quality,current_file=current_file,new_file=new_file)
                MovieDB().update_unique_id(unique_id=unique_id,movie_id=int(id),message_id=int(file_id),quality=quality,exten=category)
                await context.bot.edit_message_text(chat_id=update.effective_chat.id,message_id=query.message.reply_to_message.message_id,text=FIND_TEXT.format(id=id,title=title,quality=quality,caption=caption,category=category,file_id=file_id,file_size=file_size),reply_markup=InlineReplyMarkup(FIND_BUTTONS()),parse_mode='HTML')
            except Exception as e:print(e)
    else:
        await update.message.delete()
        await update.message.reply_to_message.delete()

        query = update.message.text
        message = update.message.reply_to_message.text.split('\n')
        file_id = int(message[0])
        bot_msg_id = int(message[1])
        current_file = message[2].split(' ')[-1]
        new_file = query
        text = f"{current_file} ->> {new_file}"
        keyboard = [[f'Confirm - EFPX1:C:sudo'],['Cancel - Close']]
        await context.bot.send_message(chat_id=update.effective_chat.id,text=text,reply_markup=InlineReplyMarkup(keyboard),reply_to_message_id=bot_msg_id)
