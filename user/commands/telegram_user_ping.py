import time

from const import Const
from datetime import datetime
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["ping", "пинг"], 1))
@pyrogram_on_error
async def pyrogram_ping(client: Client, message: Message):
    """
    :param name: Ping
    :param level: 1
    :param command: .. ping
    :param description: Отобразит время задержки
    """
    date = str(message.date).split(" ")[0].split("-") + str(message.date).split(" ")[1].split(":")
    date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
    unixtime = time.mktime(date.timetuple())
    ping_total = str('%.2f' % (time.time() - unixtime)).replace("-", "")
    return await client.xxx.method.edit(message, f"`[Ping]` {Const.EARTH} PingTime {ping_total} sec.")
