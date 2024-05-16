from tortoise import Model, fields


class Bots(Model):
    id = fields.IntField(pk=True)
    bot = fields.BigIntField(default=0)
    token = fields.TextField(max_length=255, default="None")
