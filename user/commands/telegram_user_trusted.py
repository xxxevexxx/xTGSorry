from const import Const
from datetime import datetime
from pyrogram.types import Message
from pyrogram import Client, filters
from user.filters import commands, trusted
from pyrogram.handlers.handler import Handler
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["trusteds", "доверенные"], 1))
@pyrogram_on_error
async def telegram_trusteds(client: Client, message: Message):
    """
    :param name: Trusted
    :param level: 7
    :param command: .. trusteds
    :param description: Отобразит лист доверенных
    """
    if len(client.xxx.user.get_trusted_list()) == 0:
        return await client.xxx.method.edit(message, f"`[Trusted]` {Const.WARNING} There is no objects in the database.")
    user_list = await client.get_users(user_ids=client.xxx.user.get_trusted_list())
    trusteds = ""
    for enum, user in enumerate(user_list):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        name = user.username if user.first_name and user.first_name is None else f"{user.first_name} {user.last_name}"
        if name is None: name = "Unknown user"
        trusteds += f"{Const.LS}{enum}{Const.PS} {Const.SS} {Const.USER}[{name}](tg://user?id={user.id})\n"
    return await client.xxx.method.edit(message, f"`[Trusted]` {Const.YES} Information about objects.\n\n{trusteds}")


@Client.on_message(commands("..", ["+trusted", "+доверенный"], 1))
@pyrogram_on_error
async def telegram_create_trusted(client: Client, message: Message):
    """
    :param name: Trusted
    :param level: 7
    :param command: .. +trusted
    :param description: Добавит в лист доверенных
    """
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Trusted]` {Const.WARNING} There is no object for the action.")
    if message.from_user.id == message.reply_to_message.from_user.id:
        return await client.xxx.method.edit(message, f"`[Trusted]` {Const.WARNING} You can't apply it on yourself.")
    if message.reply_to_message.from_user.id in client.xxx.user.get_trusted_list():
        return await client.xxx.method.edit(message, f"`[Trusted]` {Const.WARNING} This user is already in the trusted list.")
    await client.xxx.user.set_trusted_list(message.reply_to_message.from_user.id, "+")
    return await client.xxx.method.edit(message, f"`[Trusted]` {Const.YES} User added to the trusted list.")


@Client.on_message(commands("..", ["-trusted", "-доверенный"], 1))
@pyrogram_on_error
async def telegram_delete_trusted(client: Client, message: Message):
    """
    :param name: Trusted
    :param level: 7
    :param command: .. -trusted
    :param description: Отобразит лист доверенных
    """
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Trusted]` {Const.WARNING} There is no object for the action.")
    if message.reply_to_message.from_user.id not in client.xxx.user.get_trusted_list():
        return await client.xxx.method.edit(message, f"`[Trusted]` {Const.WARNING} This user is not in the trusted list.")
    await client.xxx.user.set_trusted_list(message.reply_to_message.from_user.id, "-")
    return await client.xxx.method.edit(message, f"`[Trusted]` {Const.YES} User delete to the trusted list.")


@Client.on_message(trusted())
@pyrogram_on_error
async def telegram_trusted(client: Client, message: Message):
    try:
        message_send = await client.send_message(
            chat_id=message.chat.id,
            text=message.text[len(client.xxx.user.get_prefix_repeats()):],
        )
        message_send.from_user = message.from_user
        message_send.from_user.id = client.me.id
        handlers = list(client.dispatcher.groups.values())[0][1:]
        for handler in handlers:
            callback = handler.callback.handlers[0][0].callback
            filters = handler.callback.handlers[0][0].filters
            if await Handler(callback, filters).check(client, message_send):
                await handler.callback.handlers[0][0].callback(client, message_send)
                break
    except: ...


