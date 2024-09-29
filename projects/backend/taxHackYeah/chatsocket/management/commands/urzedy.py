import os
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from chatsocket.models import OfficeCode

class Command(BaseCommand):
    help = 'Importuje dane urzędów skarbowych z pliku XSD do bazy danych'

    def add_arguments(self, parser):
        # Oczekujemy jednego argumentu - ścieżki do pliku XSD
        parser.add_argument('xsd_file_path', type=str, help='Ścieżka do pliku XSD z danymi urzędów skarbowych')

    def handle(self, *args, **options):
        xsd_file_path = options['xsd_file_path']

        if not os.path.exists(xsd_file_path):
            self.stderr.write(self.style.ERROR(f"Plik {xsd_file_path} nie istnieje"))
            return

        self.stdout.write(self.style.SUCCESS(f"Rozpoczęto import z pliku: {xsd_file_path}"))

        # Parsowanie pliku XSD
        try:
            tree = ET.parse(xsd_file_path)
            root = tree.getroot()

            # Definicja przestrzeni nazw (xmlns)
            namespaces = {
                'xsd': 'http://www.w3.org/2001/XMLSchema'
            }

            # Znajdowanie wszystkich elementów 'enumeration'
            for enumeration in root.findall(".//xsd:enumeration", namespaces):
                # Pobieranie kodu urzędu
                code = enumeration.attrib['value']

                # Pobieranie nazwy urzędu
                name = enumeration.find(".//xsd:documentation", namespaces).text

                # Dodawanie lub aktualizacja w bazie danych
                obj, created = OfficeCode.objects.get_or_create(code=code, defaults={'name': name})

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Dodano urząd: {name} ({code})"))
                else:
                    self.stdout.write(self.style.WARNING(f"Urząd już istnieje: {name} ({code})"))

            self.stdout.write(self.style.SUCCESS("Import zakończony pomyślnie!"))

        except ET.ParseError as e:
            self.stderr.write(self.style.ERROR(f"Błąd podczas parsowania pliku XSD: {e}"))
