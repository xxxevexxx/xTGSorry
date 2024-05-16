from models.usermodel import Users, Aliases


class AliasManager:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None
        self.aliases = {}

    async def init(self):
        self.user = await Users.filter(user=self.user_id).first()
        data = await Aliases.filter(user=self.user).all()
        for alias in data:
            self.aliases[alias.name] = {
                "name": alias.name,
                "command": alias.command,
            }

    def get_alias(self, alias):
        return self.aliases[alias]["command"]

    async def set_alias(self, alias: dict):
        self.aliases[alias["name"]] = alias
        await Aliases.create(
            user=self.user,
            name=alias["name"],
            command=alias["command"]
        )

    async def del_alias(self, name: str):
        del self.aliases[name]
        await Aliases.filter(user=self.user, name=name).delete()
