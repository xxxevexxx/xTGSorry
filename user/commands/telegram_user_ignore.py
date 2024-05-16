from const import Const
from pyrogram.types import Message
from pyrogram import Client, filters
from user.filters import commands, ignore
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["ignores", "игнор"], 1))
@pyrogram_on_error
async def telegram_ignores(client: Client, message: Message):
    """
    :param name: Ignore
    :param level: 5
    :param command: .. ignores
    :param description: Отобразит игнор лист
    """
    if len(client.xxx.user.get_ignore_list()) == 0:
        return await client.xxx.method.edit(message, f"`[Ignore]` {Const.WARNING} There is no objects in the database.")
    user_list = await client.get_users(user_ids=client.xxx.user.get_ignore_list())
    ignores = ""
    for enum, user in enumerate(user_list):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        name = user.username if user.first_name and user.first_name is None else f"{user.first_name} {user.last_name}"
        if name is None: name = "Unknown user"
        ignores += f"{Const.LS}{enum}{Const.PS} {Const.SS} {Const.USER}[{name}](tg://user?id={user.id})\n"
    return await client.xxx.method.edit(message, f"`[Ignore]` {Const.YES} Information about objects.\n\n{ignores}")


@Client.on_message(commands("..", ["+ignore", "+игнор"], 1))
@pyrogram_on_error
async def telegram_create_ignore(client: Client, message: Message):
    """
    :param name: Ignore
    :param level: 5
    :param command: .. +ignore
    :param description: Добавит в игнор лист
    """
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Ignore]` {Const.WARNING} There is no object for the action.")
    if message.from_user.id == message.reply_to_message.from_user.id:
        return await client.xxx.method.edit(message, f"`[Ignore]` {Const.WARNING} You can't apply it on yourself.")
    if message.reply_to_message.from_user.id in client.xxx.user.get_ignore_list():
        return await client.xxx.method.edit(message, f"`[Ignore]` {Const.WARNING} This user is already in the ignore list.")
    await client.xxx.user.set_ignore_list(message.reply_to_message.from_user.id, "+")
    return await client.xxx.method.edit(message, f"`[Ignore]` {Const.YES} User added to the ignore list.")


@Client.on_message(commands("..", ["-ignore", "-игнор"], 1))
@pyrogram_on_error
async def telegram_delete_ignore(client: Client, message: Message):
    """
    :param name: Ignore
    :param level: 5
    :param command: .. -ignore
    :param description: Удалит из игнор листа
    """
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Ignore]` {Const.WARNING} There is no object for the action.")
    if message.reply_to_message.from_user.id not in client.xxx.user.get_ignore_list():
        return await client.xxx.method.edit(message, f"`[Ignore]` {Const.WARNING} This user is not in the ignore list.")
    await client.xxx.user.set_ignore_list(message.reply_to_message.from_user.id, "-")
    return await client.xxx.method.edit(message, f"`[Ignore]` {Const.YES} User delete to the ignore list.")



@Client.on_message(ignore())
@pyrogram_on_error
async def telegram_ignore(client: Client, message: Message):
    try: await client.delete_messages(chat_id=message.chat.id, message_ids=message.id, revoke=False)
    except: ...
