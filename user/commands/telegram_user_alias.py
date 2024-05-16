from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["+alias", "+алиас"], 1))
@pyrogram_on_error
async def pyrogram_create_alias(client: Client, message: Message):
    """
    :param name: Alias
    :param level: 3
    :param command: .. +alias
    :param description: Создаст новый алиас
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} You must specify a name.")
    if len(message.text.split("\n")) < 2:
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} You must specify the message.")
    command = message.text.split("\n", maxsplit=1)[1]
    name = message.text.split("\n")[0].split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} Maximum length of an object name.")
    if name in list(client.xxx.alias.aliases.keys()):
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} This name is already taken.")
    await client.xxx.alias.set_alias(dict(name=name, command=command))
    return await client.xxx.method.edit(message, f"`[Alias]` {Const.YES} A new object has been created.")


@Client.on_message(commands("..", ["-alias", "-алиас"], 1))
@pyrogram_on_error
async def pyrogram_remove_alias(client: Client, message: Message):
    """
    :param name: Alias
    :param level: 3
    :param command: .. -alias
    :param description: Удалит имеющийся алиас
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} You must specify a name.")
    if message.text.split(" ")[2].lower() not in list(client.xxx.alias.aliases.keys()):
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} This name is already taken.")
    await client.xxx.alias.del_alias(message.text.split(" ")[2].lower())
    return await client.xxx.method.edit(message, f"`[Alias]` {Const.YES} An old object was deleted.")


@Client.on_message(commands("..", ["aliase", "алиасы"], 1))
@pyrogram_on_error
async def pyrogram_aliase(client: Client, message: Message):
    """
    :param name: Alias
    :param level: 3
    :param command: .. aliase
    :param description: Отобразит список алиасов
    """
    if len(client.xxx.alias.aliases) == 0:
        return await client.xxx.method.edit(message, f"`[Alias]` {Const.WARNING} There is no objects in the database.")
    aliases = ""
    for enum, alias in enumerate(client.xxx.alias.aliases.items()):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        aliases += f"""`{Const.LS}{enum}{Const.PS} {Const.FF} [{alias[0]}] {Const.SS} [{alias[1]["command"]}]`\n"""
    return await client.xxx.method.edit(message, f"`[Alias]` {Const.YES} Information about objects.\n\n{aliases}")

