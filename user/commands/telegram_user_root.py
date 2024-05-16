import subprocess

from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["root", "рут"], 5))
@pyrogram_on_error
async def pyrogram_root(client: Client, message: Message):
    """
    :param name: Root
    :param level: 1
    :param command: .. root
    :param description: Отправит команду в консоль
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Root]` {Const.WARNING} You must specify a command.")
    await client.xxx.method.edit(message, f"`[Root]` {Const.YES} Successfully send root command.")
    result = subprocess.run(" ".join(message.text.split(" ")[2:]), capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        return await client.xxx.method.edit(message, f"`[Root]` {Const.YES} Error executing the root command.\n\n{result.stderr}")
    else:
        return await client.xxx.method.edit(message, f"`[Root]` {Const.YES} Successfully send root command.\n\n{result.stdout}")