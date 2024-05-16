from const import Const
from pyrogram.types import Message
from pyrogram.enums import ChatType
from pyrogram import Client, filters
from user.filters import commands, trigger
from pyrogram.handlers.handler import Handler
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["triggers", "триггеры"], 1))
@pyrogram_on_error
async def pyrogram_triggers(client: Client, message: Message):
    """
    :param name: Trigger
    :param level: 6
    :param command: .. triggers
    :param description: Отобразит список триггеров
    """
    if len(client.xxx.trigger.triggers) == 0:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} There is no objects in the database.")
    triggers = ""
    for enum, trigger in enumerate(client.xxx.trigger.triggers.items()):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        triggers += f"""`{Const.LS}{enum}{Const.PS} {Const.FF} [{trigger[0]}] {Const.SS} {trigger[1]['trigger']} {Const.SS} [{trigger[1]['command']}]`\n"""
    return await client.xxx.method.edit(message, f"`[Trigger]` {Const.YES} Information about objects.\n\n{triggers}")


@Client.on_message(commands("..", ["+trigger", "+триггер"], 1))
@pyrogram_on_error
async def pyrogram_create_trigger(client: Client, message: Message):
    """
    :param name: Trigger
    :param level: 6
    :param command: .. +trigger
    :param description: Создаст новый триггер
    """
    if len(message.text.split("\n")[0].split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} You must specify a name.")
    name = message.text.split("\n")[0].split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} Maximum length of an object name.")
    if name in list(client.xxx.trigger.triggers.keys()):
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} This name is already taken.")
    if len(message.text.split("\n")) < 2:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} Specify a list of trigger words.")
    trigger = message.text.lower().split("\n")[1].split("/")
    if len(message.text.split("\n")) < 3:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} Specify the command when activating the trigger.")
    command = message.text.split("\n", maxsplit=2)[2]
    await client.xxx.trigger.set_trigger(
        dict(name=name, trigger=trigger, command=command)
    )
    return await client.xxx.method.edit(message, f"`[Trigger]` {Const.YES} A new object has been created.")


@Client.on_message(commands("..", ["-trigger", "-триггер"], 1))
@pyrogram_on_error
async def pyrogram_remove_trigger(client: Client, message: Message):
    """
    :param name: Trigger
    :param level: 6
    :param command: .. -trigger
    :param description: Удалит имеющийся триггер
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} You must specify a name.")
    name = message.text.split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} Maximum length of an object name.")
    if name not in list(client.xxx.trigger.triggers.keys()):
        return await client.xxx.method.edit(message, f"`[Trigger]` {Const.WARNING} This name is already taken.")
    await client.xxx.trigger.del_trigger(name)
    return await client.xxx.method.edit(message, f"`[Trigger]` {Const.YES} An old object was deleted.")


@Client.on_message(trigger())
@pyrogram_on_error
async def pyrogram_trigger(client: Client, message: Message):
    try:
        message_send = await client.send_message(
            chat_id=message.chat.id,
            text=message.text,
        )
        message_send.from_user = message.from_user
        message_send.from_user.id = client.me.id
        handlers = list(client.dispatcher.groups.values())[0][1:]
        for handler in handlers:
            callback = handler.callback.handlers[0][0].callback
            filters = handler.callback.handlers[0][0].filters
            if await Handler(callback, filters).check(client, message_send):
                await handler.callback.handlers[0][0].callback(client, message_send)
                break
    except: ...
