from update import update_and_migrate

#update_and_migrate()

import asyncio
import fastapi
import uvicorn
import subprocess

from loguru import logger
from views import labeleres
from tortoise import Tortoise
from models.botmodel import Bots
from models.usermodel import Users
from bot.controller import BotController
from datetime import datetime, timedelta
from user.controller import UserController
from utils import encrypt_data, decrypt_data
from fastapi.middleware.cors import CORSMiddleware
from config import TORTOISE_ORM, ProjectVar, ProjectConfig


app = fastapi.FastAPI()

for views in labeleres:
    app.include_router(views)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def restarter():
    while True:
        await asyncio.sleep(30)
        if ProjectVar.UPTIME + timedelta(minutes=5) < datetime.now():
            timenow = datetime.now()
            if timenow.hour == 6 and timenow.minute == 0:
                subprocess.run(["systemctl", "restart", "xTGSorry"])


@app.on_event("startup")
async def on_startup_tortoise():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    logger.info("DataBase startup")


@app.on_event("startup")
async def on_startup_bots():
    if not await Bots.filter(bot=ProjectConfig.BOT_ID).first():
        await Bots.create(bot=ProjectConfig.BOT_ID, token=encrypt_data(ProjectConfig.BOT_TOKEN))
    for bot_data in await Bots.all():
        bot = BotController(bot_data.bot)
        ProjectVar.BOTS[bot_data.bot] = bot
        if not await ProjectVar.BOTS[bot_data.bot].init():
            del ProjectVar.BOTS[bot_data.bot]
    logger.info(f"Groups startup - [Quantity - {len(ProjectVar.BOTS)}]")


@app.on_event("startup")
async def on_startup_users():
    for user_data in await Users.all():
        user = UserController(user_data.user)
        ProjectVar.USERS[user_data.user] = user
        if not await ProjectVar.USERS[user_data.user].init():
            del ProjectVar.USERS[user_data.user]
    logger.info(f"Users startup - [Quantity - {len(ProjectVar.USERS)}]")


@app.on_event("startup")
async def on_startup_restart():
    asyncio.create_task(restarter())
    datetimenow = datetime.now()
    next_six_am = datetime(datetimenow.year, datetimenow.month, datetimenow.day, 6, 0)
    if datetimenow >= next_six_am: next_six_am += timedelta(days=1)
    restart = next_six_am - datetimenow
    logger.info(f"Restarter startup: restart via [{restart}]")


@app.on_event("shutdown")
async def on_shutdown_users():
    for user_data in await Users.all():
        if ProjectVar.USERS.get(user_data.user):
            await ProjectVar.USERS[user_data.user].stop()
    logger.info("Users shutdown")


@app.on_event("shutdown")
async def on_shutdown_bots():
    for bot_data in await Bots.all():
        if ProjectVar.BOTS.get(bot_data.bot):
            await ProjectVar.BOTS[bot_data.bot].stop()
    logger.info("Bots shutdown")


@app.on_event("shutdown")
async def on_shutdown_tortoise():
    await Tortoise.close_connections()
    logger.info("Base shutdown")


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=666, log_level="debug")
