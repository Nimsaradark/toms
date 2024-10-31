import asyncio
from Easy_Bot import do_task
from Easy_Bot.ext import ContextTypes

@do_task
async def delete_scheduler(context: ContextTypes.DEFAULT_TYPE, message_id: int, chat_id: int, time: int):
    await asyncio.sleep(time)
    try:await context.bot.delete_message(chat_id=chat_id,message_id=message_id)
    except:pass
    
