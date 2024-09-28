import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ChatSockets(AsyncWebsocketConsumer):

    async def connect(self):
        # token = self.scope['query_string'].decode().split('token=')[1]
        try:
            # user, _ = JWTAuthentication().authenticate_credentials(token.encode())
            # self.scope['user'] = user
            await self.accept()
        except AuthenticationFailed:
            await self.close()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print('Received message:', message)
        await self.send(text_data=json.dumps({
            'message': message
        }))
