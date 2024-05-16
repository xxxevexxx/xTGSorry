from pyrogram.types import Message


class Methods:

    def __init__(self, client):
        self.client = client

    async def send(self, message: Message, for_id: int, text: str):
        return await self.client.send_message(
            chat_id=for_id,
            text=text
        )

    async def edit(self, message: Message, text: str):
        return await self.client.edit_message_text(
            message_id=message.id,
            chat_id=message.chat.id,
            text=text
        )

    async def delete(self, message: Message):
        return await self.client.delete_messages(
            chat_id=message.chat.id,
            message_ids=message.id
        )
