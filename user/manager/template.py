from models.usermodel import Users, Templates


class TemplateManager:

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None
        self.templates = {}

    async def init(self):
        self.user = await Users.filter(user=self.user_id).first()
        data = await Templates.filter(user=self.user).all()
        for template in data:
            self.templates[template.name] = {
                "name": template.name,
                "media": template.media,
                "message_id": template.message_id
            }

    def get_template(self, template):
        return self.templates[template]

    async def set_template(self, template: dict):
        self.templates[template["name"]] = template
        await Templates.create(
            user=self.user,
            name=template["name"],
            media=template["media"],
            message_id=template["message_id"]
        )

    async def del_template(self, name: str):
        del self.templates[name]
        await Templates.filter(user=self.user, name=name).delete()
