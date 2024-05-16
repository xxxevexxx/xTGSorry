from pyrogram import filters
from config import ProjectVar
from pyrogram.enums import ChatType


def commands(prefix, command, rank):

    async def func(flt, client, message):

        if not client.xxx.user.get_rank() >= flt.rank: return False

        if not bool(message.from_user and message.from_user.is_self or getattr(message, "outgoing", False)):
            return False

        if bool(message.forward_date) and bool(message.scheduled):
            return False

        message.text = message.text or message.caption
        if message.text is None: return False
        if message.from_user is None: return False

        if message.text.split(" ")[0].lower() in list(client.xxx.alias.aliases.keys()):
            alias_command = client.xxx.alias.get_alias(message.text.split(" ")[0].lower())
            message.text = message.text.replace(message.text.split(" ")[0], alias_command)

        message.command = message.text.split("\n")[0].split(" ")
        if len(message.command) < 2: return False

        accept_command_list = ["connect", "disconnect", "привязать", "отвязать"]
        if message.chat.type != ChatType.PRIVATE and message.command[1] not in accept_command_list:
            if message.chat.id not in client.xxx.user.get_chats_list(): return False

        if isinstance(flt.prefix, str):
            flt.prefix = [flt.prefix]
        if ".." in flt.prefix: flt.prefix = ["..", client.xxx.user.get_prefix_commands()]
        if ",," in flt.prefix: flt.prefix = [",,", client.xxx.user.get_prefix_scripts()]

        result = bool(message.command[0].lower() in flt.prefix and message.command[1].lower() in flt.command)
        if result: await client.xxx.user.set_command_time()
        return result

    return filters.create(func, prefix=prefix, command=command, rank=rank)


def trigger():

    async def func(_, client, message):

        message.text = message.text or message.caption
        if message.text is None: return
        if message.from_user is None: return False
        if message.from_user.id == client.xxx.user_id: return

        if message.chat.type not in [ChatType.BOT, ChatType.GROUP, ChatType.PRIVATE, ChatType.SUPERGROUP]: return False

        if bool(message.from_user and message.from_user.is_self or getattr(message, "outgoing", False)):
            return False

        if message.chat.type != ChatType.PRIVATE:
            if message.chat.id not in client.xxx.user.get_chats_list():
                return

        for trigger in list(client.xxx.trigger.triggers.keys()):
            if message.text.lower() in client.xxx.trigger.triggers[trigger]["trigger"]:
                message.text = client.xxx.trigger.triggers[trigger]["command"]
                return True
        return False

    return filters.create(func)


def trusted():

    async def func(_, client, message):

        prefix = client.xxx.user.get_prefix_repeats()

        message.text = message.text or message.caption
        if message.from_user is None: return False
        if message.text is None: return

        if message.chat.type not in [ChatType.BOT, ChatType.GROUP, ChatType.PRIVATE, ChatType.SUPERGROUP]: return False

        if message.from_user.id not in client.xxx.user.get_trusted_list(): return False

        if len(message.text) <= len(prefix): return False

        return message.text[:len(prefix)] == prefix

    return filters.create(func)


def ignore():

    async def func(_, client, message):

        if message.from_user is None: return False

        if message.chat.type not in [ChatType.BOT, ChatType.GROUP, ChatType.PRIVATE, ChatType.SUPERGROUP]: return False

        return message.from_user.id in client.xxx.user.get_ignore_list()

    return filters.create(func)
