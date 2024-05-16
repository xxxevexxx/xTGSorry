from functools import wraps
from config import ProjectVar
from pyrogram.errors import BadRequest, Forbidden, SeeOther, Unauthorized, NotAcceptable, FloodWait, InternalServerError


def pyrogram_on_error(func):
    @wraps(func)
    async def wrapper(client, message):
        try:
            error_message = (
                f"`[MESSAGE]` **Text: < {message.text} > | ItsMe: {str(client.me.id == message.from_user.id)}**\n"
                f"`[USERINFO]` **Пользователь с ID: {client.me.id}**\n"
                "`[{error_type}]` "
                f"**{func.__name__.upper()}: "
                "{error_text}**\n"
            )
            try:
                return await func(client, message)
            except SeeOther as error:
                error_message = error_message.replace(
                    "{error_type}", "SeeOther"
                ).replace("{error_text}", str(error))
            except FloodWait as error:
                error_message = error_message.replace(
                    "{error_type}", "FloodWait"
                ).replace("{error_text}", str(error))
            except Forbidden as error:
                error_message = error_message.replace(
                    "{error_type}", "Forbidden"
                ).replace("{error_text}", str(error))
            except BadRequest as error:
                error_message = error_message.replace(
                    "{error_type}", "BadRequest"
                ).replace("{error_text}", str(error))
            except Unauthorized as error:
                error_message = error_message.replace(
                    "{error_type}", "Unauthorized"
                ).replace("{error_text}", str(error))
            except NotAcceptable as error:
                error_message = error_message.replace(
                    "{error_type}", "NotAcceptable"
                ).replace("{error_text}", str(error))
            except InternalServerError as error:
                error_message = error_message.replace(
                    "{error_type}", "InternalServerError"
                ).replace("{error_text}", str(error))
            except Exception as error:
                error_message = error_message.replace(
                    "{error_type}", "Exception"
                ).replace("{error_text}", str(error))
            try:
                print(error_message)
                await ProjectVar.BOTS[5665110498].client.send_message(chat_id=890678178, text=error_message)
            except: ...
        except Exception as error:
            try:
                await ProjectVar.BOTS[5665110498].client.send_message(chat_id=890678178, text=f"{error}\n")
                with open("log.txt", "w") as file:
                    file.write(f"{message.__dict__}\n")
            except: ...

    return wrapper
