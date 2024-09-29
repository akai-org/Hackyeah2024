import re
from lxml import etree
from datetime import datetime
from .errors import FieldInvalid, FieldRequired, FieldOneof
from .validators import Validator

class Generator(Validator):
    def generate_xml(self,data):
        data = data.copy()
        for key, value in data.items():
            if value is not None:
                if isinstance(value, str):
                    if value.strip() == "" or value.strip().upper() == "NULL":
                        data[key] = None
    
        root = etree.Element("Deklaracja", xmlns="http://crd.gov.pl/wzor/2023/12/13/13064/")
    
        naglowek = etree.SubElement(root, "Naglowek")
        kod_formularza = etree.SubElement(naglowek, "KodFormularza",
                                          kodSystemowy="PCC-3 (6)",
                                          kodPodatku="PCC",
                                          rodzajZobowiazania="Z",
                                          wersjaSchemy="1-0E")
        kod_formularza.text = "PCC-3"
    
        wariant_formularza = etree.SubElement(naglowek, "WariantFormularza")
        wariant_formularza.text = "6"
    
        cel_zlozenia = etree.SubElement(naglowek, "CelZlozenia", poz="P_6")
        cel_zlozenia.text = "1"
    
        data_zlozenia = etree.SubElement(naglowek, "Data", poz="P_4")
        data_zlozenia.text = self.h_required(data['Data dokonania czynności'], "data dokonania czynności")
        try:
            datetime_object = datetime.strptime(data_zlozenia.text, '%Y-%m-%d')
            if datetime.strptime("2024-01-01", '%Y-%m-%d') > datetime_object:
                raise FieldInvalid('data dokonania czynności nie może być starsza niż 2024-01-01')
        except:
            raise FieldInvalid('data dokonania czynności')
    
        kod_urzedu = etree.SubElement(naglowek, "KodUrzedu")
        kod_urzedu.text = self.h_required(data['Urząd Skarbowy dla miejscowości'], "urząd skarbowy właściwy dla miejscowości")
    
        # Podmiot1
        podmiot1 = etree.SubElement(root, "Podmiot1", rola="Podatnik")
        czy_osoba_fizyczna = True
        if czy_osoba_fizyczna:
            osoba_fizyczna = etree.SubElement(podmiot1, "OsobaFizyczna")
    
            pesel = etree.SubElement(osoba_fizyczna, "PESEL")
            pesel.text = self.h_required(data['PESEL'], "PESEL")
    
            imie = etree.SubElement(osoba_fizyczna, "ImiePierwsze")
            imie.text = self.h_required(data['Imię'], "imię")
    
            nazwisko = etree.SubElement(osoba_fizyczna, "Nazwisko")
            nazwisko.text = self.h_required(data['Nazwisko'], "nazwisko")
    
            data_urodzenia = etree.SubElement(osoba_fizyczna, "DataUrodzenia")
            if data['Data urodzenia'] is None:
                year = int(pesel.substr(0, 2))
                month = int(pesel.substr(2, 2))
                day = int(pesel.substr(4, 2))
                code = month / 20
                month = month - 20 * code
                year = year + ((code + 1) % 5 - 1) * 100 + 1900
                data['Data urodzenia'] = str(year) + "-" + str(month) + "-" + str(day)
            data_urodzenia.text = self.h_required(data['Data urodzenia'], "data urodzenia")
    
            if data['Imię ojca'] is not None:
                imieojca = etree.SubElement(osoba_fizyczna, "ImieOjca")
                imieojca.text = data['Imię ojca']
            if data['Imię matki'] is not None:
                imiematki = etree.SubElement(osoba_fizyczna, "ImieMatki")
                imiematki.text = data['Imię matki']
        else:
            osoba_niefizyczna = etree.SubElement(podmiot1, "OsobaNiefizyczna")
            nip = etree.SubElement(osoba_niefizyczna, "NIP")
            nip.text = self.h_required(data['NIP'], "NIP")
            if not self.czy_nip_prawidlowy(nip.text):
                raise FieldInvalid('numer nip jest nieprawidłowy')
    
            namefull = etree.SubElement(osoba_niefizyczna, "Nazwa pełna identyfikująca spółkę/firmę/osobę niefizyczną")
            namefull.text = self.h_required(data['Nazwa pełna identyfikująca spółkę/firmę/osobę niefizyczną'],
                                       "pełna nazwa spółki/firmy/osoby niefizycznej")
            if len(namefull.text) < 1:
                raise FieldInvalid('pełna nazwa spółki/firmy/osoby niefizycznej jest zbyt krótka')
            if len(namefull.text) > 240:
                raise FieldInvalid('pełna nazwa spółki/firmy/osoby niefizycznej jest zbyt długa (ponad 240 znaków)')
    
            nameshort = etree.SubElement(osoba_niefizyczna, "Nazwa skrócona identyfikująca spółkę/firmę/osobę niefizyczną")
            nameshort.text = self.h_required(data['Nazwa skrócona identyfikująca spółkę/firmę/osobę niefizyczną'],
                                        "skrócona nazwa spółki/firmy/osoby niefizycznej")
            if len(nameshort.text) < 1:
                raise FieldInvalid('skrócona nazwa spółki/firmy/osoby niefizycznej jest zbyt krótka')
            if len(nameshort.text) > 70:
                raise FieldInvalid('skrócona nazwa spółki/firmy/osoby niefizycznej jest zbyt długa (ponad 70 znaków)')
    
        # Adres zamieszkania
        adres = etree.SubElement(podmiot1, "AdresZamieszkaniaSiedziby", rodzajAdresu="RAD")
        czy_polski = data['Czy polski adres'] == "Tak"
        if czy_polski:
            adres_pol = etree.SubElement(adres, "AdresPol")
        else:
            adres_pol = etree.SubElement(adres, "AdresZagr")
    
        kod_kraju = etree.SubElement(adres_pol, "KodKraju")
        kod_kraju.text = self.h_required(data['Kraj'], 'kod kraju')
        if (czy_polski and kod_kraju.text != "PL") or (
                not czy_polski and not re.match(r"^(P[A-KM-Z])|([A-OQ-Z][A-Z])$", kod_kraju.text)):
            raise FieldInvalid("kod kraju")
    
        wojewodztwo = etree.SubElement(adres_pol, "Wojewodztwo")
        wojewodztwo.text = data['Województwo']
    
        powiat = etree.SubElement(adres_pol, "Powiat")
        powiat.text = data['Powiat']
    
        gmina = etree.SubElement(adres_pol, "Gmina")
        gmina.text = data['Gmina']
    
        if data['Ulica'] is not None:
            ulica = etree.SubElement(adres_pol, "Ulica")
            ulica.text = data['Ulica']
    
        if data['Numer domu'] is not None:
            nr_domu = etree.SubElement(adres_pol, "NrDomu")
            nr_domu.text = data['Numer domu']
    
        if data['Numer lokalu'] is not None:
            nr_lokalu = etree.SubElement(adres_pol, "NrLokalu")
            nr_lokalu.text = data['Numer lokalu']
    
        miejscowosc = etree.SubElement(adres_pol, "Miejscowosc")
        miejscowosc.text = data['Miejscowość']
    
        if data['Kod pocztowy'] is not None:
            kod_pocztowy = etree.SubElement(adres_pol, "KodPocztowy")
            kod_pocztowy.text = data['Kod pocztowy']
    
        # Pozycje Szczegolowe
        pozycje = etree.SubElement(root, "PozycjeSzczegolowe")
        p_7 = etree.SubElement(pozycje, "P_7")
        p_7.text = self.h_oneof(data['Rodzaj czynności cywilnoprawnej'],
                           {'Podmiot zobowiązany solidarnie do zapłaty podatku': "1",
                            'Strona umowy zamiany': "2",
                            'Wspólnik spółki cywilnej': "3",
                            'Podmiot, o którym mowa w art. 9 pkt 10 lit. b ustawy (pożyczkobiorca)': "4",
                            'Inny podmiot - różny od: podmiotu zobowiązanego solidarnie do zapłaty podatku, strony umowy zamiany, wspólnika spółki cywilnej': "5",
                            }, 'podmiot składający deklarację')
    
        p_20 = etree.SubElement(pozycje, "P_20")
        p_20.text = self.h_oneof(
            data['Przedmiot opodatkowania (umowa/zmiana umowy/orzeczenie sądu/inne)'],
            {
                'umowa': "1",
                'zmiana umowy': "2",
                'orzeczenie sądu lub ugoda': "3",
                'inne': "4",
            },
            "przedmiot opodatkowania (umowa/zmiana umowy/orzeczenie sądu/inne)"
        )
    
        if data['Miejsce położenia rzeczy lub miejsce wykonywania prawa majątkowego terytorium polski lub nie'] is not None:
            p_21 = etree.SubElement(pozycje, "P_21")
            p_21.text = self.h_oneof(
                data['Miejsce położenia rzeczy lub miejsce wykonywania prawa majątkowego terytorium polski lub nie'],
                {
                    'terytorium RP': "1",
                    'poza terytorium RP': "2",
                },
                "Miejsce położenia rzeczy lub miejsce wykonywania prawa majątkowego"
            )
    
        if data['Miejsce dokonania czynności cywilnoprawnej terytorium polski lub nie'] is not None:
            p_22 = etree.SubElement(pozycje, "P_22")
            p_22.text = self.h_oneof(
                data['Miejsce dokonania czynności cywilnoprawnej terytorium polski lub nie'],
                {
                    'terytorium RP': "1",
                    'poza terytorium RP': "2",
                },
                "Miejsce dokonania czynności cywilnoprawnej"
            )
    
        p_23 = etree.SubElement(pozycje, "P_23")
        p_23.text = self.h_required(data['Treść i przedmiot czynności cywilnoprawnej'],
                               "Treść i przedmiot czynności cywilnoprawnej")
    
        stawka_podatku = self.h_required(data['Stawka podatku określona zgodnie z art. 7 ustawy'],
                                    'Stawka podatku określona zgodnie z art. 7 ustawy')
        stawka_podatku = self.h_good_int(stawka_podatku.replace("%", ""), "Stawka podatku określona zgodnie z art. 7 ustawy")
    
        kwota_czynnosci = self.h_required(data['Kwota czynności PLN / Podstawa opodatkowania PLN'],
                                     'Kwota czynności PLN / Podstawa opodatkowania PLN')
        kwota_czynnosci = self.h_good_int(kwota_czynnosci, "Kwota czynności PLN / Podstawa opodatkowania PLN")
    
        kwota_suma = 0
    
        if p_20.text == "1":
            p_24 = etree.SubElement(pozycje, "P_24")
            p_24.text = kwota_czynnosci
    
            p_25 = etree.SubElement(pozycje, "P_25")
            p_25.text = str(int(int(kwota_czynnosci) * 0.01))
    
            kwota_suma = kwota_suma + int(int(kwota_czynnosci) * 0.01)
    
        if stawka_podatku == "2":
            p_26 = etree.SubElement(pozycje, "P_26")
            p_26.text = kwota_czynnosci
    
            p_27 = etree.SubElement(pozycje, "P_27")
            p_27.text = str(int(int(kwota_czynnosci) * 0.02))
    
            kwota_suma = kwota_suma + int(int(kwota_czynnosci) * 0.02)
    
        if p_20.text == "2":  # zmiana umowy:
            p_28 = etree.SubElement(pozycje, "P_28")
            p_28.text = kwota_czynnosci
    
            p_29 = etree.SubElement(pozycje, "P_29")
            p_29.text = stawka_podatku
    
            p_30 = etree.SubElement(pozycje, "P_30")
            p_30.text = str(int(int(kwota_czynnosci) * (int(stawka_podatku) / 100.0)))
    
            kwota_suma = kwota_suma + int(int(kwota_czynnosci) * (int(stawka_podatku) / 100.0))
    
        if p_20.text == "4":  # inna
            P_43A = etree.SubElement(pozycje, "P_43A")
            P_43A.text = "inne"
    
            p_43 = etree.SubElement(pozycje, "P_43")
            p_43.text = kwota_czynnosci
    
            p_44 = etree.SubElement(pozycje, "P_44")
            p_44.text = stawka_podatku
    
            p_45 = etree.SubElement(pozycje, "P_45")
            p_45.text = str(int(int(kwota_czynnosci) * (int(stawka_podatku) / 100.0)))
    
            kwota_suma = kwota_suma + int(int(kwota_czynnosci) * (int(stawka_podatku) / 100.0))
    
        p_46 = etree.SubElement(pozycje, "P_46")
        p_46.text = str(kwota_suma)  # Wartość podatku
    
        p_53 = etree.SubElement(pozycje, "P_53")
        p_53.text = str(kwota_suma)  # Kwota podatku
    
        p_62 = etree.SubElement(pozycje, "P_62")
        p_62.text = "1"
        pouczenia = etree.SubElement(root, "Pouczenia")
        pouczenia.text = "1"
        xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        xml.decode("utf-8")
        with open(f"{datetime.now()}.xml", "wb") as f:
            f.write(xml)
        return xml