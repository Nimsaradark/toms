from Easy_Bot import bot
from Easy_Bot.ext import Client , HANDLERS , MessagesHandlers , ContextTypes

from Database import connect_database
from Handlers import button_handler , message_text_handler , message_document_handler
from Config import TOKEN , WEBHOOK_URL , PORT
from Plugins.Chat_manager import greet_chat_members

async def main():
    Bot = bot(TOKEN)
    bot_name = ((await Bot.get_me()).first_name)
    connect_database(bot_name)
    

if __name__ == '__main__':
    app = Client(
        token = TOKEN ,
        webhook_url = WEBHOOK_URL,
        port = PORT,
        handlers = HANDLERS(
            commands = 'bot/Commands',
        
            messages=MessagesHandlers(
                text=message_text_handler,
                document=message_document_handler,
            ),
        
            callback=button_handler,
            greeting=greet_chat_members,
            start_function=main,
            )
        )
    app.start()
