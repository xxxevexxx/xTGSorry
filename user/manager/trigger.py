from models.usermodel import Users, Triggers


class TriggerManager:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None
        self.triggers = {}

    async def init(self):
        self.user = await Users.filter(user=self.user_id).first()
        data = await Triggers.filter(user=self.user).all()
        for trigger in data:
            self.triggers[trigger.name] = {
                "name": trigger.name,
                "trigger": trigger.trigger,
                "command": trigger.command,
            }

    def get_trigger(self, trigger):
        return self.triggers[trigger]

    async def set_trigger(self, trigger: dict):
        self.triggers[trigger["name"]] = trigger
        await Triggers.create(
            user=self.user,
            name=trigger["name"],
            trigger=trigger["trigger"],
            command=trigger["command"],
        )

    async def del_trigger(self, name: str):
        del self.triggers[name]
        await Triggers.filter(user=self.user, name=name).delete()
