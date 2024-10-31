def START_MSG_KEYBOARD(user_id: int) -> list:
    return [
        [f"ʜᴇʟᴘ ᴀɴᴅ ғᴇᴀᴛᴜʀᴇs - M7T5Z:{user_id}"],
        [" ɪɴꜰɪɴɪᴛʏ ᴍᴏᴠɪᴇꜱ - https://t.me/InfinityMovieslk","sᴜᴘᴘᴏʀᴛ - https://t.me/+OfGlGQXx-dY2ZWRl"],
    ]

def HELP_MSG_KEYBOARD(user_id: int) -> list:
    return [
        [f"ᴜᴘᴅᴀᴛᴇs - https://t.me/infinity_updates",f"ᴅᴇᴠᴇʟᴏᴘᴇʀ - J4P6L:{user_id}"],
        [f"ᴄʟᴏsᴇ - Close:{user_id}"],
    ]

def FORCE_SUB_KEYBOARD(link: str) -> list:
    return [
        [f"Join Now - {link}"]
    ]

def LEECH_BUTTONS() -> list:
    return [
        ['Leech - leech:sudo'],
        ['Close - close:sudo']
    ]


def ADD_TV_BUTTONS(chat_id) -> list:
    return [
        [f'Add to Database - addtv:{chat_id}:sudo']
    ]
    
def FIND_BUTTONS() -> list:
    return [
        ['Edit - EDBX2::sudo'],
        ['Delete - DELX12:sudo']
    ]
    
def EDIT_DB_BUTTONS(file_id,movie_id):
    return[
        [f'Title - ETPX1:{movie_id}:sudo',f'Quality - EQPX1:S:{file_id}:sudo'],
        [f'Caption - ECPX1:{file_id}:sudp',f'FIle - EFPX1:S:{movie_id}:sudo'],
        ['Back - BDBX1:sudo']
    ]

def DELETE_BUTTONS(file_id,movie_id):
    return[
        [f'Confirm - DLXF41:{file_id}:{movie_id}'],
        ['Cancel - BDBX1:sudo']
    ]

def GREETING_BUTTONS():
    return [['🌱 Join Now 🌱 - https://t.me/infinity_updates']]


def DOWNLOAD_BUTTON():
    return [['🔰 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 𝐅𝐫𝐨𝐦 𝐇𝐞𝐫𝐞 🔰 - https://t.me/InfinityMovieslk']]
