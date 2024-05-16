from const import Const
from user.filters import commands
from pyrogram.types import Message
from collections import OrderedDict
from pyrogram import Client, filters
from user.decorators import pyrogram_on_error


@Client.on_message(commands("..", ["команды", "commands"], 1))
@pyrogram_on_error
async def pyrogram_commands(client: Client, message: Message):
    """
    :param name: Command
    :param level: 1
    :param command: .. commands
    :param description: Отобразит список команд
    """
    module = {}
    command = ""
    for items in client.xxx.commands:
        if module.get(items['level']):
            module[items['level']].append(items)
        else:
            module[items['level']] = [items]

    module = OrderedDict(sorted(module.items(), key=lambda x: int(x[0])))
    for items in list(module.keys()):
        module[items] = sorted(module[items], key=lambda x: len(x['name']))

    for enum, items in enumerate((module.keys())):
        if enum == 0:
            command += f"— Main:\n"
        else:
            command += f"— {module[items][0]['name']}:\n"
        for item in module[items]:
            command += f"- {Const.LS}{item['name']}{Const.PS} {Const.SS} {item['command']} | {item['description']}\n"
        command += "\n"
    return await client.xxx.method.edit(message, command)
