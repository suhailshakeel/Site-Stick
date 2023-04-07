import random, asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
        self.is_connected = True
        
        while self.is_connected:
            await asyncio.sleep(1)
            await self.send(f'[{random.randint(1,10)}, {random.randint(1,10)}]')

    async def disconnect(self, close_code):
        self.is_connected = False
        raise StopConsumer()