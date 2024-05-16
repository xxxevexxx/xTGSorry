import asyncio
import pyrostep

from loguru import logger
from pyrogram import Client
from utils import decrypt_data
from config import ProjectConfig
from models.botmodel import Bots


class BotController:

    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.polling = None
        self.client = None

    async def init(self):
        data = await Bots.filter(bot=self.bot_id).first()
        try:
            await self.session(data)
            self.polling = BotPolling(self.client)
            await self.polling.start()
        except Exception as error:
            logger.info(f"[BOT] Error init request: {error}")
            return False
        else:
            logger.info(f"[BOT] Success init request: {self.bot_id}")
            return True

    async def session(self, data):
        self.client = Client(
            in_memory=True,
            bot_token=decrypt_data(data.token),
            name=f"bot_{data.bot}",
            api_id=ProjectConfig.CLIENT_ID,
            api_hash=ProjectConfig.CLIENT_HASH,
            plugins=dict(root="bot/commands")
        )
        pyrostep.listen(self.client)

    async def start(self):
        try:
            await self.polling.start()
            logger.info(f"[BOT] Success start request: {self.bot_id}")
            return True
        except Exception as error:
            logger.error(f"[BOT] Error start request: {error}")
            return False

    async def stop(self):
        try:
            await self.polling.stop()
            logger.info(f"[BOT] Success stop request: {self.bot_id}")
            return True
        except Exception as error:
            logger.error(f"[BOT] Error stop request: {error}")
            return False

    async def restart(self):
        try:
            await self.polling.restart()
            logger.info(f"[BOT] Success restart request: {self.bot_id}")
            return True
        except Exception as error:
            logger.error(f"[BOT] Error restart request: {error}")
            return False


class BotPolling:

    def __init__(self, client):
        self.client = client

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.stop()

    async def restart(self):
        await self.stop()
        await self.start()
