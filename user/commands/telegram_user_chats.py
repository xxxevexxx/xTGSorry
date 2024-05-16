from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["connect", "привязать"], 1))
@pyrogram_on_error
async def pyrogram_connect(client: Client, message: Message):
    """
    :param name: Chats
    :param level: 2
    :param command: .. connect
    :param description: Привяжет бота к чату
    """
    if message.chat.id in client.xxx.user.get_chats_list():
        return await client.xxx.method.edit(message, f"`[Chats]` {Const.WARNING} This chat is already linked.")
    await client.xxx.user.set_chats_list(message.chat.id, "+")
    return await client.xxx.method.edit(message, f"`[Chats]` {Const.YES} The chat has been successfully linked.")


@Client.on_message(commands("..", ["disconnect", "отвязать"], 1))
@pyrogram_on_error
async def pyrogram_disconnect(client: Client, message: Message):
    """
    :param name: Chats
    :param level: 2
    :param command: .. disconnect
    :param description: Отвяжет бота от чата
    """
    if message.chat.id not in client.xxx.user.get_chats_list():
        return await client.xxx.method.edit(message, f"`[Chats]` {Const.WARNING} This chat is not linked.")
    await client.xxx.user.set_chats_list(message.chat.id, "-")
    return await client.xxx.method.edit(message, f"`[Chats]` {Const.YES} The chat was successfully disabled.")


@Client.on_message(commands("..", ["clear", "очистить"], 1))
@pyrogram_on_error
async def pyrogram_clear(client: Client, message: Message):
    """
    :param name: Chats
    :param level: 2
    :param command: .. clear
    :param description: Очистит список привязанных чатов
    """
    if len(client.xxx.user.get_chats_list()) == 0:
        return await client.xxx.method.edit(message, f"`[Chats]` {Const.WARNING} There are no linked chats.")
    for chat_id in list(client.xxx.user.get_chats_list()):
        await client.xxx.user.set_chats_list(chat_id, "-")
    return await client.xxx.method.edit(message, f"`[Chats]` {Const.YES} The list of linked chats has been cleared.")