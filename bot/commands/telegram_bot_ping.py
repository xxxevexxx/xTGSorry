import time

from const import Const
from datetime import datetime
from pyrogram import Client, filters
from bot.decorators import pyrogram_on_error


@Client.on_message(filters.command("ping", "/"))
@pyrogram_on_error
async def pyrogram_ping(client, message):
    date = str(message.date).split(" ")[0].split("-") + str(message.date).split(" ")[1].split(":")
    date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
    unixtime = time.mktime(date.timetuple())
    ping_total = str('%.2f' % (time.time() - unixtime)).replace("-", "")
    return await client.send_message(
        chat_id=message.chat.id,
        text=f"{Const.EARTH} PingTime {ping_total} sec."
    )
