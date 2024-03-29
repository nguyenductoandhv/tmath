import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TypoRoomConsumer(AsyncJsonWebsocketConsumer):
    groups = ['typeroom']

    async def connect(self):
        pk = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'room_%s' % pk

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, message,
        )

    async def change_user(self, event):
        await self.send_json({
            "type": "change-user",
        })

    async def start_typo(self, event):
        await self.send_json({
            "type": "start-typo",
        })


class TypoContestConsumer(AsyncJsonWebsocketConsumer):
    groups = ['typo_contest']

    async def connect(self):
        pk = self.scope['url_route']['kwargs']['pk']
        self.room_group_name = 'contest_%s' % pk

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, message,
        )

    async def change_progress_participation(self, event):
        await self.send_json({
            "type": "change-progress",
            "message": event['message'],
        })
