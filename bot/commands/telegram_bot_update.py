import time
import pyrostep

from utils import encrypt_data
from models.usermodel import Users
from pyrogram import Client, filters
from user.controller import UserController
from config import ProjectConfig, ProjectVar
from bot.decorators import pyrogram_on_error
from pyrogram.errors import FloodWait, SessionPasswordNeeded, BadRequest


@Client.on_message(filters.private & filters.command("update", "/"))
@pyrogram_on_error
async def pyrogram_update(client, message):
    if await Users.filter(user=message.from_user.id).first() is None:
        return await client.send_message(
            chat_id=message.chat.id,
            text="You are not registered."
        )
    client.create_dict = dict(user_app=None, user_hash=None, user_code=None, user_pass=None, user_phone=None)
    await pyrostep.register_next_step(
        message.from_user.id,
        pyrogram_number
    )
    return await client.send_message(
        chat_id=message.chat.id,
        text="Send your phone."
    )


@pyrogram_on_error
async def pyrogram_number(client, message):
    client.create_dict["user_phone"] = message.text
    client.create_dict["user_app"] = Client(
        in_memory=True,
        name=f"user_{message.from_user.id}",
        api_id=ProjectConfig.CLIENT_ID,
        api_hash=ProjectConfig.CLIENT_HASH,
        phone_number=client.create_dict["user_phone"]
    )
    await client.create_dict["user_app"].connect()
    try:
        client.create_dict["user_hash"] = await client.create_dict["user_app"].send_code(client.create_dict["user_phone"])
        client.create_dict["user_hash"] = client.create_dict["user_hash"].phone_code_hash
    except FloodWait as error:
        await client.create_dict["user_app"].disconnect()
        converted_time = time.strftime(
            '%H H %M M %S S',
            time.gmtime(error.value)
        )
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"Limit, wait: {converted_time}"
        )
    await pyrostep.register_next_step(
        message.from_user.id,
        pyrogram_code
    )
    return await client.send_message(
        chat_id=message.chat.id,
        text="Send your code, format 0-0-0-0-0."
    )


@pyrogram_on_error
async def pyrogram_code(client, message):
    client.create_dict["user_code"] = message.text.replace("-", "")
    try:
        await client.create_dict["user_app"].sign_in(
            phone_code=client.create_dict["user_code"],
            phone_number=client.create_dict["user_phone"],
            phone_code_hash=client.create_dict["user_hash"]
        )
    except SessionPasswordNeeded:
        await pyrostep.register_next_step(
            message.from_user.id,
            pyrogram_pass
        )
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"Send your pass."
        )
    except BadRequest:
        await pyrostep.register_next_step(
            message.from_user.id,
            pyrogram_code
        )
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"Incorrect code, repeat."
        )
    else:
        await client.send_message(
            chat_id=message.chat.id,
            text=f"Success"
        )
    user_data = await client.create_dict["user_app"].get_me()
    if user_data.id != message.from_user.id:
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"You can only register your account."
        )
    if ProjectVar.USERS.get(user_data.id):
        await ProjectVar.USERS[user_data.id].stop()
        del ProjectVar.USERS[user_data.id]
    token = await client.create_dict["user_app"].export_session_string()
    await Users.filter(user=user_data.id).update(user=user_data.id, token=token)
    user = UserController(user_data.id)
    ProjectVar.USERS[user_data.id] = user
    await ProjectVar.USERS[user_data.id].init()


@pyrogram_on_error
async def pyrogram_pass(client, message):
    client.create_dict["user_pass"] = message.text
    try:
        await client.create_dict["user_app"].check_password(client.create_dict["user_pass"])
    except BadRequest:
        await pyrostep.register_next_step(
            message.from_user.id,
            pyrogram_pass
        )
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"Incorrect pass, repeat."
        )
    else:
        await client.send_message(
            chat_id=message.chat.id,
            text=f"Success"
        )
    user_data = await client.create_dict["user_app"].get_me()
    if user_data.id != message.from_user.id:
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"You can only register your account."
        )
    if ProjectVar.USERS.get(user_data.id):
        await ProjectVar.USERS[user_data.id].stop()
        del ProjectVar.USERS[user_data.id]
    token = await client.create_dict["user_app"].export_session_string()
    await Users.filter(user=user_data.id).update(user=user_data.id, token=encrypt_data(token))
    user = UserController(user_data.id)
    ProjectVar.USERS[user_data.id] = user
    await ProjectVar.USERS[user_data.id].init()
