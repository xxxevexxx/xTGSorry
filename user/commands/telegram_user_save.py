from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["save", "сохранить"], 1))
@pyrogram_on_error
async def pyrogram_save(client: Client, message: Message):
    """
    :param name: Saver
    :param level: 1
    :param command: .. save
    :param description: Сохранит сообщение в избранное
    """
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Saver]` {Const.WARNING} The forwarded message is missing.")
    if message.reply_to_message.media_group_id:
        await client.copy_media_group(
            chat_id=message.from_user.id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
    else:
        await client.copy_message(
            chat_id=message.from_user.id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
    return await client.xxx.method.edit(message, f"`[Saver]` {Const.YES} Successfully save this object.")
