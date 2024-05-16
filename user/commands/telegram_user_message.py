from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["message", "сообщение"], 1))
@pyrogram_on_error
async def pyrogram_message(client: Client, message: Message):
    """
    :param name: Message
    :param level: 1
    :param command: .. message
    :param description: Отправит сообщение в ЛС
    """
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Message]` {Const.WARNING} The forwarded message is missing.")
    if len(message.text.split("\n", maxsplit=1)) < 2:
        return await client.xxx.method.edit(message, f"`[Message]` {Const.WARNING} You must specify the text of the message.")
    text = message.text.split("\n", maxsplit=1)[1]
    if message.reply_to_message.from_user.is_bot:
        return await client.xxx.method.edit(message, f"`[Message]` {Const.WARNING} You can't send a message to a bot.")
    await client.xxx.method.send(message, message.reply_to_message.from_user.id, text)
    return await client.xxx.method.edit(message, f"`[Message]` {Const.YES} Successfully save this object.")
