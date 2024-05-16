from datetime import datetime
from models.usermodel import Users


class UserManager:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None
        self.nick = None
        self.rank = None
        self.balance = None
        self.register = None
        self.chats_list = None
        self.ignore_list = None
        self.trusted_list = None
        self.dialogue_list = None
        self.prefix_commands = None
        self.prefix_scripts = None
        self.prefix_repeats = None
        self.message_time = None
        self.command_time = None

    async def init(self):
        self.user = await Users.filter(user=self.user_id).first()
        self.nick = self.user.nick
        self.rank = self.user.rank
        self.balance = self.user.balance
        self.register = self.user.register
        self.chats_list = set(self.user.chats_list)
        self.ignore_list = set(self.user.ignore_list)
        self.trusted_list = set(self.user.trusted_list)
        self.dialogue_list = set(self.user.dialogue_list)
        self.prefix_commands = self.user.prefix_commands
        self.prefix_scripts = self.user.prefix_scripts
        self.prefix_repeats = self.user.prefix_repeats

    def get_nick(self) -> str:
        return self.nick

    async def set_nick(self, user_id: int, nick: str):
        self.nick = nick
        await Users.filter(user=user_id).update(nick=self.nick)

    def get_rank(self) -> str:
        return self.rank

    async def set_rank(self, user_id: int, rank: int):
        self.rank = rank
        await Users.filter(user=user_id).update(rank=self.rank)

    def get_balance(self) -> str:
        return self.balance

    async def set_balance(self, balance: int, action: str):
        balance = self.balance + balance if action == "+" else self.balance - balance
        self.balance = balance
        await Users.filter(user=self.user_id).update(balance=self.balance)

    def get_chats_list(self) -> list:
        return self.chats_list

    async def set_chats_list(self, chat_id: int, action: str):
        self.chats_list.add(chat_id) if action == "+" else self.chats_list.remove(chat_id)
        await Users.filter(user=self.user_id).update(chats_list=list(self.chats_list))

    def get_ignore_list(self) -> list:
        return self.ignore_list

    async def set_ignore_list(self, user_id: int, action: str):
        self.ignore_list.add(user_id) if action == "+" else self.ignore_list.remove(user_id)
        await Users.filter(user=self.user_id).update(ignore_list=list(self.ignore_list))

    def get_trusted_list(self) -> list:
        return self.trusted_list

    async def set_trusted_list(self, user_id: int, action: str):
        self.trusted_list.add(user_id) if action == "+" else self.trusted_list.remove(user_id)
        await Users.filter(user=self.user_id).update(trusted_list=list(self.trusted_list))

    def get_dialogue_list(self) -> list:
        return self.dialogue_list

    async def set_dialogue_list(self, user_id: int, action: str):
        self.dialogue_list.add(user_id) if action == "+" else self.dialogue_list.remove(user_id)
        await Users.filter(user=self.user_id).update(dialogue_list=list(self.dialogue_list))

    def get_prefix_commands(self) -> str:
        return self.prefix_commands

    async def set_prefix_commands(self, prefix: str, user_id: int = None):
        self.prefix_commands = prefix
        await Users.filter(user=self.user_id if not user_id else user_id).update(prefix_commands=self.prefix_commands)

    def get_prefix_scripts(self) -> str:
        return self.prefix_scripts

    async def set_prefix_scripts(self, prefix: str, user_id: int = None):
        self.prefix_scripts = prefix
        await Users.filter(user=self.user_id if not user_id else user_id).update(prefix_scripts=self.prefix_scripts)

    def get_prefix_repeats(self) -> str:
        return self.prefix_repeats

    async def set_prefix_repeats(self, prefix: str, user_id: int = None):
        self.prefix_repeats = prefix
        await Users.filter(user=self.user_id if not user_id else user_id).update(prefix_repeats=self.prefix_repeats)

    def get_command_time(self) -> datetime:
        return self.command_time

    async def set_command_time(self):
        self.command_time = datetime.now()
        await Users.filter(user=self.user_id).update(command_time=self.command_time)

    def get_message_time(self) -> datetime:
        return self.message_time

    async def set_message_time(self):
        self.message_time = datetime.now()
        await Users.filter(user=self.user_id).update(message_time=self.message_time)
