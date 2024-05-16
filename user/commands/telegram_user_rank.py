from const import Const
from user.filters import commands
from models.usermodel import Users
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["rank", "ранг"], 5))
@pyrogram_on_error
async def pyrogram_rank(client: Client, message: Message):
    """
        :param name: Rank
        :param level: 1
        :param command: .. rank
        :param description: Установит ранг пользователю
        """
    ranks = {"1": "User", "2": "Helper", "3": "Moderator", "4": "Administrator"}
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Rank]` {Const.WARNING} The forwarded message is missing.")
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Rank]` {Const.WARNING} Required parameter is missing.")
    if message.text.split(" ")[2] not in ranks:
        return await client.xxx.method.edit(message, f"`[Rank]` {Const.WARNING} Incorrect rank was passed.")
    rank = int(message.text.split(" ")[2])
    if not await Users.filter(user=message.reply_to_message.from_user.id).first():
        return await client.xxx.method.edit(message, f"`[Rank]` {Const.WARNING} This user is not registered.")
    await client.xxx.user.set_rank(message.reply_to_message.from_user.id, rank)
    return await client.xxx.method.edit(
        message, f"`[Rank]` {Const.YES} User rank set to {ranks[str(rank)]}"
    )
