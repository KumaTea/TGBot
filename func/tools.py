from typing import Optional
from pyrogram.types import Message


def get_content(message: Message) -> Optional[str]:
    text = message.text
    content_index = text.find(' ')
    # reply = message.reply_to_message
    if content_index == -1:
        # no text
        # if not reply:
        return None
    return text[content_index + 1:]
