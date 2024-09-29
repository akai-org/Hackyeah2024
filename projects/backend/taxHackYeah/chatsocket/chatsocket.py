import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.defaultfilters import first
from rest_framework.exceptions import AuthenticationFailed
from .integrations import InputValidation,GeneralTaxAssistance
from .generators import Generator
from .errors import FieldInvalid, FieldRequired, FieldOneof
class ChatSockets(AsyncWebsocketConsumer):
    first_message = True
    PCC_3 = False
    async def connect(self):
        self.chat_bot = GeneralTaxAssistance()
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

    async def receive(self,text_data):
        if len(text_data) > 1000:
            await self.send(text_data=json.dumps({
                'message': 'Message is too long'
            }))


        try:
            print(text_data)
            text_data_json = json.loads(text_data)
            print(text_data_json)
            message = text_data_json.get('message')
            mode = text_data_json.get('mode')
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'message': 'Invalid JSON'
            }))
            return
        if message is not None:
            input_validation = InputValidation(message)
            if not input_validation.is_user_input_valid():
                await self.send(text_data=json.dumps({
                    'message': 'Invalid input'
                }))
                return



        if (mode is not None and mode == "PCC-3") or self.PCC_3:
            self.PCC_3 = True
            generator = Generator()
            answer = self.chat_bot.parse_user_details(first_message=self.first_message,message=message)
            self.first_message = False
            # await self.send(text_data=json.dumps({
            #     'message': answer
            # }))
            print("PRasowamfaw: ", answer)
            try:
                xml = generator.generate_xml(answer)

            except FieldInvalid as e:
                await self.send(text_data=json.dumps({
                    'message': "Podaj proszę " + str(e)
                }))
            except FieldRequired as e:
                await self.send(text_data=json.dumps({
                    'message': "Potrzebuję informacji o " + str(e)
                }))
            except FieldOneof as e:
                await self.send(text_data=json.dumps({
                    'message': "Czego dotyczy " + str(e) + "?"
                }))
            finally:
                return
        else:
            message = self.chat_bot.process(first_message=self.first_message, message=None)
            self.first_message = False

        if message is None:
            message = "To nie twoja wina, ale coś poszło nie tak"

        await self.send(text_data=json.dumps({
            'message': message
        }))
