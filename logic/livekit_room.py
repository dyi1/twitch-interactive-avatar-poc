import os
from livekit import rtc

class LivekitRoom:
    def __init__(self):
        self.room = rtc.Room()

    async def connect(self, url, token):
        await self.room.connect(url, token)
        print(f"name: {self.room.name}")

    async def disconnect(self):
        await self.room.disconnect()