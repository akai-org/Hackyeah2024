from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from django.apps import apps


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

    def is_user_input_valid(self):
        try:
            response = self.client.moderations.create(
                model="omni-moderation-latest",
                input=self.data,
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

    def process(self,first_message) -> str|None:
        try:
            print(self.data,1)
            if first_message:
                thread = self.client.beta.threads.create()
            message = self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=self.data,
            )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id="asst_pW8xH03z83PsHw4fugran4sM",
            )
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
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

class AdministrationTerr:
    def __init__(self):
        pass

    def find_gmina(self, powiat):
        gmina = apps.get_model('chatsocket', 'gmina')
        obj = gmina.objects.filter(nazwa=powiat)
        if obj:
            return  obj[0].powiat.name, obj[0].powiat.voievodeship.name
        return None

    def find_powiat(self, voievodeship):
        powiat = apps.get_model('chatsocket', 'powiat')
        obj = powiat.objects.filter(nazwa=voievodeship)
        if obj:
            return obj[0].voievodeship.name
        return None

    def find_office(self, code):
        office = apps.get_model('chatsocket', 'officecode')
        obj = office.objects.filter(code=code)
        if obj:
            return obj[0].name
        return None

    def find_office_by_name(self, name):
        office = apps.get_model('chatsocket', 'officecode')
        obj = office.objects.filter(name=name.Upper())
        if obj:
            return obj[0].code
        return None
