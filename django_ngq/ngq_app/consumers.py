from channels.generic.websocket import AsyncWebsocketConsumer
import json

class UpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "updates"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def update_message(self, event):
        context = event['context']  # The dict being passed
        # Send the dict as JSON
        await self.send(text_data=json.dumps(context))