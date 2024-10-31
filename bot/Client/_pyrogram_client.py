from pyrogram import Client, filters 
# from _config import TOKEN , API_ID , API_HASH
from typing import Union, Optional
from pyrogram.types import Message

TOKEN = '6974189205:AAE91jLrE_e4gES1ea-0vHeSx0Ejzlxu6og'
API_ID = 17426055
API_HASH = '7ed73b9d1b9e0d58dcf734d37290f57c'


from dataclasses import dataclass

@dataclass
class message:
    id: int
    title: Optional[str]
    size : int

class _Bot(Client):

    def __init__(self):
        super().__init__(
            name="Professor-Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=TOKEN,
            workers=200,
            # sleep_threshold=10,
        )

    async def start(self):
        await super().start()

            
    async def stop(self, *args):
        await super().stop()
       
    async def iter_messages(self, chat_id: Union[int, str], last_message_id: int, start_message_i: int = 0,messages: list = []) -> list[message]:                       
        current = start_message_i
        while True:
            new_diff = min(10, last_message_id - current)
            if new_diff <= 0:break
            for msg in await self.get_messages(chat_id, list(range(current, current+new_diff+1))):
                try:messages.append(message(id=msg.id,title=msg.caption,size=round((msg.document.file_size or msg.video.file_size)/1024/1024,2))) if not msg.empty and msg.caption != None else None
                except Exception as e:
                    print(e)
                    pass
                current += 1
        
        return messages



pybot = _Bot()




