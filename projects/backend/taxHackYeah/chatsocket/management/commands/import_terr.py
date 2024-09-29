import pandas as pd
from datetime import datetime
from django.apps import apps
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import CSV data into the database'

    def handle(self, *args, **kwargs):
        self.save_to_database()

    def open_csv(self):
        df = pd.read_csv('C:\\Users\\patro\\akai\\Hackyeah2024\\projects\\backend\\taxHackYeah\\chatsocket\\management\\commands\\data.csv', on_bad_lines='skip', sep=';')
        return df

    def get_voivodeships(self, df):
        voivodeships = df.loc[df['POW'].isnull() & df['GMI'].isnull()]
        return voivodeships

    def get_POWs(self, df):
        POWs = df.loc[df['GMI'].isnull() & df['POW'].notnull()]
        return POWs

    def get_GMIs(self, df):
        GMIs = df.loc[df['POW'].notnull() & df['GMI'].notnull()]
        return GMIs

    def save_to_database(self):
        file = self.open_csv()

        Voievodeship = apps.get_model('chatsocket', 'Voievodeship')
        Powiat = apps.get_model('chatsocket', 'Powiat')
        Gmina = apps.get_model('chatsocket', 'Gmina')

        # voivodeships = self.get_voivodeships(file)
        # for index, row in voivodeships.iterrows():
        #     print(row)
        #     Voievodeship.objects.create(
        #         id=row['WOJ'],
        #         name=row['NAZWA'],
        #         on_date=datetime.now().date()
        #     )

        # POWs = self.get_POWs(file)
        # for index, row in POWs.iterrows():
        #     voivodeship = Voievodeship.objects.get(id=row['WOJ'])
        #     Powiat.objects.create(
        #         id=row['POW'],
        #         name=row['NAZWA'],
        #         voievodeship=voivodeship,
        #         on_date=datetime.now().date()
        #     )
        #
        # # Insert GMIs into the database
        GMIs = self.get_GMIs(file)
        for index, row in GMIs.iterrows():
            powiat = Powiat.objects.get(id=row['POW'])
            Gmina.objects.create(
                name=row['NAZWA'],
                powiat=powiat,
                on_date=datetime.now().date()
            )

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
