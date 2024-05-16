from config import ProjectVar
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException
from models.usermodel import Users, Aliases, Triggers, Templates


router = APIRouter()


def account_data(user: Users):
    return dict(
        nick=user.nick,
        rank=user.rank,
        balance=user.balance,
        register=user.register,
        chats_list=user.chats_list,
        ignore_list=user.ignore_list,
        trusted_list=user.trusted_list,
        dialogue_list=user.dialogue_list,
        prefix_commands=user.prefix_commands,
        prefix_scripts=user.prefix_scripts,
        prefix_repeats=user.prefix_repeats,
        message_time=user.message_time,
        command_time=user.command_time,
    )


@router.get("/account/{owner_id}/{user_id}")
async def views_get_account(request: Request, owner_id: int, user_id: int):
    user = await Users.filter(user=user_id, owner=owner_id).first()
    if user is None: return HTTPException("Account not found")
    aliases = list(await Aliases.filter(user=user).values())
    triggers = list(await Triggers.filter(user=user).values())
    templates = list(await Templates.filter(user=user).values())
    data = dict(user_id=user_id, user=account_data(user), aliases=aliases, triggers=triggers, templates=templates)
    return dict(status=True, data=data, description="Success get account")


@router.get("/accounts/{owner_id}/{limit}")
async def views_get_accounts(request: Request, owner_id: int, limit: int):
    response_accounts = []
    accounts = await Users.filter(owner=owner_id).all()
    for account in accounts:
        prefixes = dict(commands=account.prefix_commands, scripts=account.prefix_scripts, repeats=account.prefix_repeats)
        if len(response_accounts) >= limit:
            response_accounts.append(dict(user_id=account.user, username=account.nick, prefixes=prefixes, state=True, lock=True))
        else:
            response_accounts.append(dict(user_id=account.user, username=account.nick, prefixes=prefixes, state=True, lock=False))
    while len(response_accounts) < 3:
        if len(response_accounts) >= limit:
            response_accounts.append(dict(user_id=0, username="", prefixes=dict(commands="", scripts="", repeats=""), state=False, lock=True))
        else:
            response_accounts.append(dict(user_id=0, username="", prefixes=dict(commands="", scripts="", repeats=""), state=False, lock=False))
    return response_accounts


@router.post("/update")
async def views_update_account(request: Request):
    data = await request.json()
    user_id = data.get("user_id")
    owner_id = data.get("owner_id")
    user = await Users.filter(user=user_id, owner=owner_id).first()
    if user is None: return HTTPException("Account not found")
    if ProjectVar.USERS.get(user_id):
        await ProjectVar.USERS.get(user_id).user.set_nick(user_id, data.get("username"))
        await ProjectVar.USERS.get(user_id).user.set_prefix_commands(data.get("prefixes").get("commands"), user_id)
        await ProjectVar.USERS.get(user_id).user.set_prefix_scripts(data.get("prefixes").get("scripts"), user_id)
        await ProjectVar.USERS.get(user_id).user.set_prefix_repeats(data.get("prefixes").get("repeats"), user_id)
    else:
        await Users.filter(user=user_id).update(
            nick=data.get("username"), 
            prefix_commands=data.get("prefixes").get("commands"),
            prefix_scripts=data.get("prefixes").get("scripts"),
            prefix_repeats=data.get("prefixes").get("repeats"),
        )
    return dict(status=True, description="Success update account")


@router.post("/action")
async def views_action_account(request: Request):
    data = await request.json()
    action = data.get("action")
    user_id = data.get("user_id")
    owner_id = data.get("owner_id")
    user = await Users.filter(user=user_id, owner=owner_id).first()
    if user is None: return HTTPException("Account not found")
    try:
        if action == "restart":
            await ProjectVar.USERS[user_id].restart()
        if action == "start":
            await ProjectVar.USERS[user_id].start()
        if action == "stop":
            await ProjectVar.USERS[user_id].stop()
    except:
        return HTTPException("Error send command")
    else:
        return dict(status=True, description="Success send command")