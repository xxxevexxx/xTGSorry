from config import ProjectVar
from pyrogram import Client, filters
from bot.decorators import pyrogram_on_error


@Client.on_message(filters.command("stop", "/"))
@pyrogram_on_error
async def pyrogram_stop(client, message):
    if ProjectVar.USERS.get(message.from_user.id):
        await ProjectVar.USERS[message.from_user.id].stop()
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"The /stop command has been sent."
        )
    else:
        return await client.send_message(
            chat_id=message.chat.id,
            text="You are not registered."
        )