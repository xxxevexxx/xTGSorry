import asyncio

from const import Const
from datetime import datetime
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["push", "пуши"], 1))
@pyrogram_on_error
async def pyrogram_push(client: Client, message: Message):
    """
    :param name: Push
    :param level: 1
    :param command: .. push
    :param description: Отобразит 3 упомянания
    """
    if client.me.username is None:
        return await client.xxx.method.edit(message, f"`[Push]` {Const.WARNING} You don't have a username set.")
    await client.xxx.method.edit(message, f"`[Push]` {Const.LOADING} Search for messages with mentions.")
    state = False
    async for message_push in client.search_messages(message.chat.id, f"@{client.me.username}", limit=3):
        try:
            await client.send_message(
                reply_to_message_id=message_push.id,
                chat_id=message.chat.id,
                text=f"⤴️",
            )
            state = True
        except: ...
        await asyncio.sleep(0.5)
    if state:
        return await client.xxx.method.edit(message, f"`[Push]` {Const.YES} Information about messages.")
    else:
        return await client.xxx.method.edit(message, f"`[Push]` {Const.YES} No messages found mentioning.")
