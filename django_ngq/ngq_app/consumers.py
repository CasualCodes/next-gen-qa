from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import threading
from channels.exceptions import StopConsumer
import time

cancel_flags = {}

class UpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.deletable = False
        # Setup
        self.group_name = "updates"
        self.session_id = self.scope["session"].session_key
        print(f"Consumers {self.session_id}")
        cancel_flags[self.session_id] = threading.Event()

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if self.session_id in cancel_flags:
            cancel_flags[self.session_id].set()
        
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("Disconnect Complete")
        raise StopConsumer() 

    async def update_message(self, event):
        context = event['context']  # The dict being passed
        # Send the dict as JSON
        await self.send(text_data=json.dumps(context))