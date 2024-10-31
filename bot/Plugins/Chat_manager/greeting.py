from typing import Optional, Tuple
from telegram import ChatMember, ChatMemberUpdated, Update
from telegram.ext import ContextTypes
from Config import JOINED_MSG , LEFT_MSG , GROUPS , GREETING_BUTTONS
from Easy_Bot import InlineReplyMarkup 


def extract_status_change(chat_member_update: ChatMemberUpdated) -> Optional[Tuple[bool, bool]]:

    status_change = chat_member_update.difference().get("status")
    old_is_member, new_is_member = chat_member_update.difference().get("is_member", (None, None))

    if status_change is None:
        return None

    old_status, new_status = status_change
    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)
    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # print(update)
    if update.effective_chat.id not in GROUPS:return
    result = extract_status_change(update.chat_member)
    if result is None:
        return

    was_member, is_member = result
    member_name = update.chat_member.new_chat_member.user.mention_html()
    reply_markup = InlineReplyMarkup(GREETING_BUTTONS())
    if not was_member and is_member:
        await update.effective_chat.send_message(
            JOINED_MSG.format(member_name=member_name),
            parse_mode='HTML',
            reply_markup=reply_markup,
        )
    elif was_member and not is_member:
        await update.effective_chat.send_message(
            LEFT_MSG.format(member_name=member_name),
            parse_mode='HTML',
            reply_markup=reply_markup,
        )

