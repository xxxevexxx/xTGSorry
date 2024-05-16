from config import ProjectVar
from pyrogram import Client, filters
from bot.decorators import pyrogram_on_error


@Client.on_message(filters.command("restart", "/"))
@pyrogram_on_error
async def pyrogram_restart(client, message):
    if ProjectVar.USERS.get(message.from_user.id):
        await ProjectVar.USERS[message.from_user.id].restart()
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"The /restart command has been sent."
        )
    else:
        return await client.send_message(
            chat_id=message.chat.id,
            text="You are not registered."
        )
