import time

from const import Const
from datetime import datetime
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["info", "инфо"], 1))
@pyrogram_on_error
async def pyrogram_info(client: Client, message: Message):
    """
    :param name: Info
    :param level: 1
    :param command: .. info
    :param description: Отображает информацию о пользователе
    """
    ranks = {"1": "User", "2": "Helper", "3": "Moderator", "4": "Administrator", "5": "SystemAdmin", "6": "Developer"}
    register_time = datetime.utcfromtimestamp(client.xxx.user.register)
    register_time = register_time.strftime("%d.%m.%Y %H:%M:%S")
    send_message = (
        f"[Info] {Const.EARTH} Information about the account.\n\n"
        f"{Const.SS} NickName: {client.xxx.user.get_nick()}\n"
        f"{Const.SS} Balance: {client.xxx.user.get_balance()}\n"
        f"{Const.SS} Rank: {ranks[str(client.xxx.user.get_rank())]}\n\n"
        f"{Const.SS} Templates: {len(client.xxx.template.templates)}\n"
        f"{Const.SS} Triggers: {len(client.xxx.trigger.triggers)}\n"
        f"{Const.SS} Aliases: {len(client.xxx.alias.aliases)}\n\n"
        f"{Const.SS} Trusteds: {len(client.xxx.user.trusted_list)}\n"
        f"{Const.SS} Ignores: {len(client.xxx.user.ignore_list)}\n"
        f"{Const.SS} Chats: {len(client.xxx.user.chats_list)}\n\n"
        f"{Const.SS} Commands: {client.xxx.user.get_prefix_commands()}\n"
        f"{Const.SS} Repeats: {client.xxx.user.get_prefix_repeats()}\n"
        f"{Const.SS} Scripts: {client.xxx.user.get_prefix_scripts()}\n\n"
        f"[Info] {Const.EARTH} Register time: {register_time}.\n\n"
    )
    return await client.xxx.method.edit(message, send_message)
