import os

from datetime import datetime
from dotenv import load_dotenv
from cryptography.fernet import Fernet


load_dotenv()


class ProjectVar:
    BOTS = {}
    USERS = {}
    CHATS = {}
    TG_AUTH = {}
    UPTIME = datetime.now()


class ProjectConfig:
    BOT_ID = os.getenv('BOT_ID')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    FERNET_TOKEN = Fernet(os.getenv('FERNET_TOKEN').encode('utf-8'))
    CLIENT_NAME = "MyProject"
    CLIENT_HASH = 'd89672a589c14e14129a713a01c86d0c'
    CLIENT_ID = 183162
    MODEL_USERS = f"models.usermodel"
    MODEL_BOTS = f"models.botmodel"
    BASES_PATH = os.getenv('BASES_PATH')
    


TORTOISE_ORM = {
    "connections": {"default": ProjectConfig.BASES_PATH},
    "apps": {
        "models": {
            "models": [ProjectConfig.MODEL_USERS, ProjectConfig.MODEL_BOTS, "aerich.models"],
            "default_connection": "default",
        },
    },
}