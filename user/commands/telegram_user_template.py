from const import Const
from user.filters import commands
from pyrogram.types import Message
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["templates", "шаблоны"], 1))
@pyrogram_on_error
async def pyrogram_templates(client: Client, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. templates
    :param description: Отобразит список шаблонов
    """
    if len(client.xxx.template.templates) == 0:
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} There is no objects in the database.")
    templates = ""
    for enum, template in enumerate(client.xxx.template.templates.items()):
        enum = enum + 1 if enum + 1 >= 10 else f"0{enum + 1}"
        templates += f"`{Const.LS}{enum}{Const.PS} {Const.FF} [{template[0]}] {Const.SS} [Template]`\n"
    return await client.xxx.method.edit(message, f"`[Template]` {Const.YES} Information about objects.\n\n{templates}")


@Client.on_message(commands("..", ["template", "шаблон"], 1))
@pyrogram_on_error
async def pyrogram_template(client: Client, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. template
    :param description: Вызовет имеющийся шаблон
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} You must specify a name.")
    if message.text.split(" ")[2].lower() not in list(client.xxx.template.templates.keys()):
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} This name is already taken.")
    template_object = client.xxx.template.get_template(message.text.split(" ")[2].lower())
    await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    if template_object["media"]:
        return await client.copy_media_group(
            chat_id=message.chat.id,
            from_chat_id=message.from_user.id,
            message_id=template_object["message_id"]
        )
    return await client.copy_message(
        chat_id=message.chat.id,
        from_chat_id=message.from_user.id,
        message_id=template_object["message_id"]
    )


@Client.on_message(commands("..", ["+template", "+шаблон"], 1))
@pyrogram_on_error
async def pyrogram_create_template(client: Client, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. +template
    :param description: Создаст новый шаблон
    """
    if len(message.text.split(" ")) < 3:
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} You must specify a name.")
    name = message.text.split(" ")[2].lower()
    if len(name) > 10:
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} Maximum length of an object name.")
    if name in list(client.xxx.template.templates.keys()):
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} This name is already taken.")
    if message.reply_to_message is None:
        return await client.xxx.method.edit(message, f"`[Template]` {Const.WARNING} Need to send template.")
    if message.reply_to_message.media_group_id:
        media = True
        message_object = await client.copy_media_group(
            chat_id=message.from_user.id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
    else:
        media = False
        message_object = await client.copy_message(
            chat_id=message.from_user.id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.id
        )
    await client.xxx.template.set_template(
        dict(name=name, media=media, message_id=message_object.id)
    )
    return await client.xxx.method.edit(message, f"`[Template]` {Const.YES} A new object has been created.")


@Client.on_message(commands("..", ["-template", "-шаблон"], 1))
@pyrogram_on_error
async def pyrogram_remove_template(client: Client, message: Message):
    """
    :param name: Template
    :param level: 8
    :param command: .. -template
    :param description: Удалит имеющийся шаблон
    """
    if len(message.text.split(" ")) < 3:
        return await client.edit_message_text(
            message_id=message.id,
            chat_id=message.chat.id,
            text=f"`[Template]` {Const.WARNING} You must specify a name."
        )
    name = message.text.split(" ")[2].lower()
    if len(name) > 10:
        return await client.edit_message_text(
            message_id=message.id,
            chat_id=message.chat.id,
            text=f"`[Template]` {Const.WARNING} Maximum length of an object name."
        )
    if name not in list(client.xxx.template.templates.keys()):
        return await client.edit_message_text(
            message_id=message.id,
            chat_id=message.chat.id,
            text=f"`[Template]` {Const.WARNING} This name is already taken."
        )
    template_object = client.xxx.template.get_template(message.text.split(" ")[2].lower())
    await client.xxx.template.del_template(name)
    await client.delete_messages(chat_id=message.from_user.id, message_ids=template_object["message_id"])
    return await client.edit_message_text(
        message_id=message.id,
        chat_id=message.chat.id,
        text=f"`[Template]` {Const.YES} An old object was deleted."
    )
