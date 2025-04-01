from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import json
import threading
from channels.exceptions import StopConsumer
import time

cancel_flags = {}

#####################
## UPDATE CONSUMER ##
#####################
# - handles updating the front end with the context data during dynamic results loading
class UpdateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Setup
        self.group_name = "updates"
        print("Connection Established")
        # self.session_id = self.scope["session"].session_key
        # print(f"Consumers {self.session_id}")
        # cancel_flags[self.session_id] = threading.Event()

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # if self.session_id in cancel_flags:
        #     cancel_flags[self.session_id].set()
        
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        print("Disconnect Complete")
        raise StopConsumer() 

    async def update_message(self, event):
        print("Updating Frontend")
        context = event['context']
        # Send the dict as JSON
        await self.send(text_data=json.dumps(context))