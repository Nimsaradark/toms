START_MSG_TEXT = """
ʜɪ {user} ʜᴏᴡ ᴀʀᴇ ʏᴏᴜ ! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ɪɴꜰɪɴɪᴛʏ ꜰᴀᴍɪʟʏ 

ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴇɴᴊᴏʏ ʙᴇꜱᴛ ᴇᴠᴇʀ ꜰɪʟᴍ ᴇxᴘᴇʀɪᴇɴᴄᴇ ɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ ᴇɴᴛᴇʀ ᴛʜᴇ ɪɴꜰɪɴɪᴛʏ ᴘᴏʀᴛᴀʟ ᴀɴᴅ ꜱᴇᴇ ᴍᴀɢɪᴄ ᴇᴠᴇʀʏᴛʜɪɴɢ ɪɴꜰɪɴɪᴛʏ

"""

HELP_MSG_TEXT = """
<b>Hi {user} 💚</b> 

<i> ʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ Today..?</i>
"""

WAITING_MSG = "<b>🧐 හිටින්න පොඩ්ඩක් හිටින්න...</b>"

ST_LOAD = 'CAACAgUAAx0CYzLM2AACPKpnHwtWsc3eL03-bWEjk59ZEqdSdgACqAEAAtYpMVRrR7iH35lQzh4E'

NO_RESULTS_MSG = """
<b>සොරි අනේ 😥, {search_query} කියලා ෆිල්ම් එකක් වත් ටිවි සීරිස් එකක්වත් මගේ Database එකේ හොයාගන්න නැ ..</b>

<b>🌱 ගොඩාක් වෙලාවට ඔයා නම වැරදියට ටයිප් කරලා ඇති එක නිසා ආයි පාරක් ෆිල්ම් එකේ හෝ සීරිස් එකේ නම හරියට "google" එකෙන් බලලා හරි එවන්න</b>

<i>💚 ඔයා හොයපු ෆිල්ම් එක හො ටිවි සීරිස් එක නැත්තම් ඇඩ්ම්න්ලාට ඔය පහත තියෙන Not Here බට්න් එකෙන් request එකක් යවන්න...</i>

"""

RESULTS_MSG = """
<b>👋 හායි {user}</b>

<b>බලන්න ඔයා හොයන {search_query} මෙතන තියෙනවද කියලා</b>

<i>📌 ඔයා හොයන්නේ සීරිස් එකක් නම් 'Series' කියන බට්න් එක ඔබලා ඔයාට ඔනි Tv Series එක තොරන්න</i>

"""

TV_RESULT = """
<b>මේ තියෙන්නේ ඔයා ඉල්ලපු <b>{title}</b> සිරීස් එක</b>

<i>🔰 යට තියෙන Download බට්න් එක ක්ලික් කරාලා චැන්ල් එකට ජොයින් වෙලා සීරිස් එක ඩව්න්ලොඩ් කරගන්න</i>

<i>🔰 දැනට ආපු සීසන් ඔක්කොම චැන්ල් එකට අප්ලොඩ් කරලා තමයි තියෙන්නේ</i>

"""

SELECT_QUALITY = "<b>හරි දැන් ඔයාට ඔනි Quality එක තොරන්නකෝ...</b>"

HERE_ARE_FILES = "<b>මේ තියෙන්නේ ඔයා ඉල්ලපු {quality} කොලිටි එකට අදාල ෆයිල්ස් 👇🏻</b>"""

FORCE_SUB_MSG_TEXT = """
{user},

<b>🧑🏻‍💻 පේන විදියට ඔයා අපේ <b><i>Update Channel</i></b> එකට Join වෙලා නැ වගේ 🤒</b>

<b>දැන් හොද ලමයා වගේ එකට ජොයින් වෙලා ඔයාට ඔනි ෆිල්ම් එක හෝ ටිවි සීරිස් එක හොයාගන්න</b>

"""

JOINED_MSG = """ 
<b>Hi {member_name}, Welcome To The Infinity Movies.!💚  I'm Sydney How Can I Help You..</b>

<i>🔰 ඔයාට ඔනි ෆීල්ම් එකේ හරි ටිවි සීරිස් එකේ හරි නම ටයිප් කරලා Group එකට Send කරන්න</i>

<b>Ex - Conjuring 2013</b>

<b>💚 ඒ වගේම පහල තියෙන Join Now button එකෙන් අපේ update චැන්ල් එකටත් සෙට් වෙන්න නැත්තම් ඔයාට අලුතින් එන ෆිල්ම් , සීරිස් මග හැරෙයි</b>

<i>🔰 එ වගේම ඔයාට මොනාහරි ගැටලුවක් තියෙනම් අපේ bot මැසෙජ් එකක් දාන්නකෝ...</i>

Feel The Infinity! 🦋

"""

LEFT_MSG = """
{member_name} is no longer with us. Thanks a lot ..."
"""


MOVIE_DETAILS_MSG_TEXT = """ 
<b>මේ තියෙන්නේ ඔයා ඉල්ලපු {file_name}</b> 

<blockquote><i>● Released Date : {released}</i></blockquote>
<blockquote><i>● Language : {languages}</i></blockquote>
<blockquote><i>● Genres :  {genres}</i></blockquote>
<blockquote><i>● IMDB : {rating}/10 ({votes} Votes)</i></blockquote>
""" 

CHANNEL_POST_MSG = """ 
<b><i>{title}</i></b> <i>now available on Infinity Movies</i>

<blockquote><i>● Released Date : {released}</i></blockquote>
<blockquote><i>● Language : {languages}</i></blockquote>
<blockquote><i>● Genres :  {genres}</i></blockquote>
<blockquote><i>● IMDB : {rating}/10 ({votes} Votes)</i></blockquote>

<b>🟢 Uploaded</b>
""" 

CHANNEL_DESCRIPTION = """
For Geeks, By Geeks
"""

BOT_TEXT = """
<i>processing</i>
"""

CHANNEL_CREATED_MSG_TEXT = """
<b><i>Channel Created</i></b>

<i>Title</i>             : <code>{title}</code>
<i>ID</i>                : <code>{id}</code>
<i>Description</i> : <code>{description}</code>
"""   

INBOX_MSG = """
<b>User :</b> {user}
<b>User ID :</b> <code>{user_id}</code>
<b>msg :</b> <code>{message}</code>
"""

DONE_MSG = """
<b>📝ඔයා ඉල්ලපු <b>{req_text}</b> සම්පුර්ණ කරලා තියෙන්නේ ඔයාට දැන් ගිහිල්ලා අපේ Group එකෙන් <i>{req_text}</i> ඩව්න්ලොඩ් කරගන්න පුලුවන්</b> 

<i> ගොඩක් ඉස්තුතියි 💚 ඔයාට මගේ Database එකේ නැති ෆිල්ම්,ටිවි සීරීස් request කරනවට.,</i>

"""

NOT_RELEASE_MSG = """
<b>❌ තාම මයා ඉල්ලපු <b>{req_text}</b> release වෙලා නැනේ මේක ආපු ගමන්ම අපි ඔයාට Update එකකින් දැනුම් දෙන්නම් 😇</b>
"""

COULDNT_FIND_MSG = """
<b>💔 සොරි අනේ ඔයා ඉල්ලපු <b>{req_text}</b> internet එකේ හොයාගන්න නැනේ. සමහරවිට ආයි පාරක් හරියට Type කරලා බලන්න</b>
"""

REGULATIONS_MSG = """
❌ I cannot Upload <b>{req_text}</b>, Because it is against my personal and  community policies.
"""

WRONG_NAME_MSG = """
<b>🪀 ඔයා ඉල්ලපු <b>{req_text}</b> කියන එකේ නම වැරදියි ආයි පාරක් හරි නම search කරලා අපේ group එකේ ගහන්න 😇</b>
"""

ALEARDY_IN_DB_MSG = """
<b>✅ <b>{req_text}</b> දැනටමත් මගේ Database එකෙ තියෙනවා එක නිසා හරියට නම Type කරලා group එකට දාන්නකෝ...</b>
"""

