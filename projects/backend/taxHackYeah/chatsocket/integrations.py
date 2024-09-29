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
        self.message = data

    def is_user_input_valid(self):
        try:
            response = self.client.moderations.create(
                model="omni-moderation-latest",
                input=self.message,
            )

            for result in response.results:
                flagged = result.flagged
                if flagged:
                    return False
        except Exception as ex:
            print("Exception", ex)
        return True




class GeneralTaxAssistance(OpenAIClient):
    def __init__(self):
        super().__init__()
        self.thread = None
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
            "Kwota czynności PLN / Podstawa opodatkowania PLN": "",
            "Data dokonania czynności": "",
            "Urząd Skarbowy dla miejscowości": "",
            "Czy jesteś osobą fizyczną": "",
            "Nazwa pełna identyfikująca spółkę/firmę/osobę niefizyczną": "",
            "Nazwa skrócona identyfikująca spółkę/firmę/osobę niefizyczną": "",
            "Czy polski adres": "",
            "Kod kraju jeśli jest inny niż Polska": "",
            "Imię ojca": "",
            "Imię matki": "",
            "Zwięzłe określenie treści i przedmiotu czynności cywilnoprawnej": "",
            "Stawka podatku określona zgodnie z art. 7 ustawy": "",
            "Przedmiot opodatkowania (umowa/zmiana umowy/orzeczenie sądu/inne)": "",
            "Miejsce położenia rzeczy lub miejsce wykonywania prawa majątkowego terytorium polski lub nie": "",
            "Miejsce dokonania czynności cywilnoprawnej terytorium polski lub nie": "",
        }

    def process(self,first_message,message) -> str|None:
        try:
            if first_message:
                self.thread = self.client.beta.threads.create()
            if message is not None:
                self.client.beta.threads.messages.create(
                    thread_id=self.thread.id,
                    role="user",
                    content=message,
                )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id="asst_pW8xH03z83PsHw4fugran4sM",
            )
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                result = messages.data[0].content[0].text.value
                return result
            else:
                print(run.status)
        except Exception as ex:
            print("Exception", ex)

        return None

    def parse_user_details(self,first_message,message) -> dict:
        my_struct = self.primary_struct.copy()
        try:
            if first_message:
                self.thread = self.client.beta.threads.create()
            # message = "Mam na imię Bartosz i chciałbym złożyć PCC-3 data zakupu samochodu to 3 września 2024 roku"
            if message is not None:
                self.client.beta.threads.messages.create(
                    thread_id=self.thread.id,
                    role="user",
                    content=message,
                )
            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=self.thread.id,
                assistant_id="asst_RYkE3qeU6i7uFB99FnVZFRG5",
            )
            if run.status == 'completed':
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread.id
                )
                result = messages.data[0].content[0].text.value
                print("RESULT: ", result)
                result = result[max(0, result.find("{")):min(len(result), result.rfind("}")+1)].strip()
                # print("result: ", result)
                data = json.loads(result)
                # print("DATA: ", data)
                for k, v in data.items():
                    if k in my_struct:
                        my_struct[k] = v
                return data
            else:
                print(run.status)
        except Exception as ex:
            print("Exception e:", ex)

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
