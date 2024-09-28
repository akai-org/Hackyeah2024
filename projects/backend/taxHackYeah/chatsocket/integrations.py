import time
import random
from openai import OpenAI
import json

from twisted.words.protocols.jabber.jstrports import client
from dotenv import load_dotenv
import os


class OpenAIClient:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )

class InputValidation(OpenAIClient):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def is_user_input_valid(self,text):
        try:
            response = self.client.moderations.create(
                model="omni-moderation-latest",
                input=text,
            )

            for result in response.results:
                flagged = result.flagged
                if flagged:
                    return False
        except Exception as ex:
            print("Exception", ex)
        return True




class GeneralTaxAssistance(OpenAIClient):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.primary_struct = {
            "Imię": "",
            "Nazwisko": "",
            "PESEL": "",
            "NIP": "",
            "Data urodzenia": "",
            "Kraj": "",
            "Województwo": "",
            "Powiat": "",
            "Gmina": "",
            "Miejscowość": "",
            "Ulica": "",
            "Numer domu": "",
            "Numer lokalu": "",
            "Kod pocztowy": "",
            "Treść i przedmiot czynności cywilnoprawnej": "",
            "Rodzaj czynności cywilnoprawnej": "",
            "Kwota czynności PLN": ""
        }

    def procces(self,text):
        try:
            thread = client.beta.threads.create()
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=text,
            )
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id="asst_pW8xH03z83PsHw4fugran4sM",
            )
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                result = messages.data[0].content[0].text.value
                return result
            else:
                print(run.status)
        except Exception as ex:
            print("Exception", ex)

        return None

    def parse_user_details(self,text):
        my_struct = self.primary_struct.copy()
        try:
            thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=text,
            )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id="asst_RYkE3qeU6i7uFB99FnVZFRG5",
            )
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                result = messages.data[0].content[0].text.value
                result = result[max(0, result.find("{")):max(len(result), result.rfind("}"))]
                data = json.loads(result)
                for k, v in data.items():
                    if k in my_struct:
                        my_struct[k] = v
                return data
            else:
                print(run.status)
        except Exception as ex:
            print("Exception", ex)

        return my_struct

    async def async_fetch(self,text:str ="") -> str:
        pass
