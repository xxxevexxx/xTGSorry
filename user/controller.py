import asyncio
import pyrostep

from loguru import logger
from pyrogram import Client
from utils import decrypt_data
from user.methods import Methods
from models.usermodel import Users
from config import ProjectConfig, ProjectVar
from user.commands import user_functions, user_commands

from user.manager.user import UserManager
from user.manager.alias import AliasManager
from user.manager.trigger import TriggerManager
from user.manager.template import TemplateManager


class UserController:

    def __init__(self, user_id):
        self.method = None
        self.polling = None
        self.user_id = user_id
        self.commands = user_commands
        self.functions = user_functions
        self.user = UserManager(self.user_id)
        self.alias = AliasManager(self.user_id)
        self.trigger = TriggerManager(self.user_id)
        self.template = TemplateManager(self.user_id)

    async def init(self):
        for func in [self.user, self.alias, self.trigger, self.template]: await func.init()
        data = await Users.filter(user=self.user_id).first()
        try:
            await self.session(data)
            self.polling = UserPolling(self.client)
            await self.polling.start()
        except Exception as error:
            logger.info(f"[USER] Error init request: {error}")
            return False
        else:
            logger.info(f"[USER] Success init request: {self.user_id}")
            return True

    async def session(self, data):
        self.client = Client(
            in_memory=True,
            session_string=decrypt_data(data.token),
            name=f"user_{data.user}",
            api_id=ProjectConfig.CLIENT_ID,
            api_hash=ProjectConfig.CLIENT_HASH,
            plugins=dict(root="user/commands")
        )
        self.method = Methods(self.client)
        setattr(self.client, "xxx", self)
        pyrostep.listen(self.client)

    async def start(self):
        try:
            await self.polling.start()
            logger.info(f"[USER] Success start request: {self.user_id}")
            return True
        except Exception as error:
            logger.error(f"[USER] Error start request: {error}")
            return False

    async def stop(self):
        try:
            await self.polling.stop()
            logger.info(f"[USER] Success stop request: {self.user_id}")
            return True
        except Exception as error:
            logger.error(f"[USER] Error stop request: {error}")
            return False

    async def restart(self):
        try:
            try: self.polling.stop()
            except: ...
            await self.init()
            try: self.polling.start()
            except: ...
            logger.info(f"[USER] Success restart request: {self.user_id}")
            return True
        except Exception as error:
            logger.error(f"[USER] Error restart request: {error}")
            return False


class UserPolling:

    def __init__(self, client):
        self.client = client

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.stop()

