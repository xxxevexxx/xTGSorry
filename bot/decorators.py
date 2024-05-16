from functools import wraps
from config import ProjectVar
from pyrogram.enums import ChatType


def pyrogram_on_error(func):
    @wraps(func)
    async def wrapper(client, message):
            try:
                if ProjectVar.CHATS.get(message.from_user.id) == message.id: return
                if message.chat.type != ChatType.PRIVATE: ProjectVar.CHATS[message.from_user.id] = message.id
                return await func(client, message)
            except Exception as error:
                ...

    return wrapper
