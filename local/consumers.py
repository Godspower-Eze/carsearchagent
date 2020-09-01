from channels.generic.websocket import AsyncWebsocketConsumer
import json


class Crawler(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = "frontpage"

        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_card):
        pass

    async def receive(self, text_data):
        data_point = json.loads(text_data)
        val = data_point['value']
        await self.channel_layer.group_send(
            self.groupname,
            {
                'type': 'processor',
                'value': val
            }
        )

    async def processor(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({'value': valOther}))


class Searcher(AsyncWebsocketConsumer):
    async def connect(self):
        self.groupname = "searchpage"

        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_card):
        pass

    async def receive(self, text_data):
        data_point = json.loads(text_data)
        val = data_point['value']
        await self.channel_layer.group_send(
            self.groupname,
            {
                'type': 'processor',
                'value': val
            }
        )

    async def processor(self, event):
        valOther = event['value']
        await self.send(text_data=json.dumps({'value': valOther}))
