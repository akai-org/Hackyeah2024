import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.exceptions import AuthenticationFailed
from .integrations import InputValidation,GeneralTaxAssistance

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
        print('Disconnected:', close_code)
        await self.close()

    async def receive(self, text_data):
        if len(text_data) > 100000:
            await self.send(text_data=json.dumps({
                'message': 'Message is too long'
            }))


        try:
            print(text_data)
            text_data_json = json.loads(text_data)
            print(text_data_json)
            message = text_data_json['message']
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'message': 'Invalid JSON'
            }))
            return
        print('Received message:', message)
        input_validation = InputValidation(message)
        if not input_validation.is_user_input_valid():
            await self.send(text_data=json.dumps({
                'message': 'Invalid input'
            }))
            return
        chat_bot = GeneralTaxAssistance(message)
        message = chat_bot.process()
        if message is None:
            message = "To nie twoja wina, ale coś poszło nie tak"

        await self.send(text_data=json.dumps({
            'message': message
        }))
