import time

from utils import encrypt_data
from models.usermodel import Users
from pyrogram import Client
from fastapi import APIRouter, Request
from user.controller import UserController
from config import ProjectConfig, ProjectVar
from pyrogram.errors import FloodWait, SessionPasswordNeeded, BadRequest, PhoneNumberInvalid


router = APIRouter()


async def tg_number(owner_id, data):
    ProjectVar.TG_AUTH[owner_id] = dict(user_app=None, user_hash=None, user_code=None, user_pass=None, user_phone=None, owner_id=owner_id)
    ProjectVar.TG_AUTH[owner_id]["user_phone"] = data
    ProjectVar.TG_AUTH[owner_id]["user_app"] = Client(
        name=f"user",
        in_memory=True,
        api_id=ProjectConfig.CLIENT_ID,
        api_hash=ProjectConfig.CLIENT_HASH,
        phone_number=ProjectVar.TG_AUTH[owner_id]["user_phone"]
    )
    await ProjectVar.TG_AUTH[owner_id]["user_app"].connect()
    try:
        ProjectVar.TG_AUTH[owner_id]["user_hash"] = await ProjectVar.TG_AUTH[owner_id]["user_app"].send_code(
            ProjectVar.TG_AUTH[owner_id]["user_phone"]
        )
        ProjectVar.TG_AUTH[owner_id]["user_hash"] = ProjectVar.TG_AUTH[owner_id]["user_hash"].phone_code_hash
    except FloodWait as error:
        await ProjectVar.TG_AUTH[owner_id]["user_app"].disconnect()
        converted_time = time.strftime('%H hour %M min %S sec.', time.gmtime(error.value))
        return dict(status=False, description=f"Повторите попытку через: {converted_time}")
    except PhoneNumberInvalid:
        await ProjectVar.TG_AUTH[owner_id]["user_app"].disconnect()
        return dict(status=False, description=f"Некорректный номер телефона")
    else:
        return dict(status=True, description=f"Введите код авторизации")


async def tg_code(owner_id, data):
    ProjectVar.TG_AUTH[owner_id]["user_code"] = data
    try:
        await ProjectVar.TG_AUTH[owner_id]["user_app"].sign_in(
            phone_code=ProjectVar.TG_AUTH[owner_id]["user_code"],
            phone_number=ProjectVar.TG_AUTH[owner_id]["user_phone"],
            phone_code_hash=ProjectVar.TG_AUTH[owner_id]["user_hash"]
        )
    except SessionPasswordNeeded:
        return dict(status=True, description=f"Введите пароль авторизации")
    except BadRequest:
        return dict(status=False, description=f"Передан не верный код, повторите")
    return await tg_token(owner_id)


async def tg_password(owner_id, data):
    ProjectVar.TG_AUTH[owner_id]["user_pass"] = data
    try:
        await ProjectVar.TG_AUTH[owner_id]["user_app"].check_password(ProjectVar.TG_AUTH[owner_id]["user_pass"])
    except BadRequest:
        return dict(status=False, description=f"Передан не верный пароль, повторите")
    return await tg_token(owner_id)


async def tg_token(owner_id):
    user_data = await ProjectVar.TG_AUTH[owner_id]["user_app"].get_me()
    user_id = user_data.id
    user_token = await ProjectVar.TG_AUTH[owner_id]["user_app"].export_session_string()
    user = await Users.filter(user=user_id).first()
    if user:
        if user.owner != owner_id: return dict(status=False, description=f"Аккаунт пренадлежит другому пользователю")
        await Users.filter(user=user_id).update(token=encrypt_data(user_token))
        if ProjectVar.USERS.get(user_id): ProjectVar.USERS[user_id].stop()
    else:
        await Users.create(user=user_id, owner=owner_id, token=encrypt_data(user_token))
    user = UserController(user_id)
    ProjectVar.USERS[user_id] = user
    await ProjectVar.USERS[user_id].init()
    return dict(status=True, description=f"Приятного пользования")


@router.post("/auth")
async def views_tgsorry_auth(request: Request):
    data = await request.json()
    owner_id = data.get("owner_id")
    action = data.get("action")
    data = data.get("data")
    if action == "tg_number":
        return await tg_number(owner_id, data)
    if action == "tg_code":
        return await tg_code(owner_id, data)
    if action == "tg_password":
        return await tg_password(owner_id, data)


