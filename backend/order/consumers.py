import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("orders", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("orders", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            "orders",
            {
                "type": "order_update",
                "message": data["message"]
            }
        )

    async def order_update(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
    async def order_completed(self, event):
        # This sends the message to the frontend
        await self.send(text_data=json.dumps({
            "type": "order_completed",
            "order_id": event["order_id"],
            "customer_name": event["customer_name"],
            "hoagie": event["hoagie"],
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.group_name = f'user_{self.user_id}_notifications'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_order_completed(self, event):
        await self.send(text_data=json.dumps({
            'type': 'order_completed',
            'order_id': event['order_id'],
            'completed_at': event['completed_at'],
            'message': 'Your order is ready!',
        }))
