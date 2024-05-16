import base64
import asyncio
from pyrogram import Client
from config import ProjectConfig
from models.usermodel import Users
from pyrogram.errors import AuthKeyUnregistered


# Кодирование данных
def encrypt_data(data):
    try:
        encrypted_data = base64.b64encode(ProjectConfig.FERNET_TOKEN.encrypt(data.encode())).decode('utf-8')
    except:
        encrypted_data = "e-e-e-e-e-e"
    return encrypted_data


# Декодирование данных
def decrypt_data(encrypted_data):
    try:
        decrypted_data = ProjectConfig.FERNET_TOKEN.decrypt(base64.b64decode(encrypted_data.encode('utf-8'))).decode()
    except:
        decrypted_data = "d-d-d-d-d-d"
    return decrypted_data