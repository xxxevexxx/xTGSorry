import asyncio

from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["deletter", "дд"], 1))
@pyrogram_on_error
async def pyrogram_deletter(client: Client, message: Message):
    """
    :param name: Deletter
    :param level: 1
    :param command: .. deletter
    :param description: Удалит последние 3 сообщения
    """
    enumerates = 0
    if len(message.text.split(" ")) < 3: value = 4
    else: value = int(message.text.split(" ")[2]) + 1
    if value > 30:
        return await client.xxx.method.edit(message, f"`[Deleter]` {Const.WARNING} Message limit exceeded.")
    async for items in client.get_chat_history(chat_id=message.chat.id):
        if items.from_user.id == message.from_user.id:
            await client.delete_messages(chat_id=message.chat.id, message_ids=items.id)
            await asyncio.sleep(0.3)
            enumerates += 1
        if enumerates == value:
            break


@Client.on_message(commands("..", ["рдд", "rdd"], 1))
@pyrogram_on_error
async def pyrogram_rdeletter(client: Client, message: Message):
    """
    :param name: RDeletter
    :param level: 1
    :param command: .. rdeletter
    :param description: Редактирует и удалит последние 3 сообщения
    """
    enumerates = 0
    if len(message.text.split(" ")) < 3:
        value = 4
    else:
        try: value = int(message.text.split(" ")[2]) + 1
        except: value = 4
    if value > 30:
        return await client.xxx.method.edit(message, f"`[Deleter]` {Const.WARNING} Message limit exceeded.")
    if len(message.text.split(" ")) < 4:
        text = f"{Const.WARNING}" * 3
    else:
        text = "".join(message.text.split(" ", maxsplit=3)[3])
    async for items in client.get_chat_history(chat_id=message.chat.id):
        if items.from_user.id == message.from_user.id:
            try: await client.edit_message_text(chat_id=message.chat.id, message_id=items.id, text=text)
            except: pass
            await asyncio.sleep(0.3)
            await client.delete_messages(chat_id=message.chat.id, message_ids=items.id)
            enumerates += 1
        if enumerates == value:
            break
