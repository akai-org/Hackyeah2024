import xml.etree.ElementTree as ET

# Funkcja tworząca XML na podstawie dostarczonego słownika
def generate_xml(data):
    # Utwórz główny element XML
    deklaracja = ET.Element("Deklaracja", xmlns="http://crd.gov.pl/wzor/2023/12/13/13064/")

    # Nagłówek
    naglowek = ET.SubElement(deklaracja, "Naglowek")
    kod_formularza = ET.SubElement(naglowek, "KodFormularza", kodSystemowy="PCC-3 (6)", kodPodatku="PCC", rodzajZobowiazania="Z", wersjaSchemy="1-0E")
    kod_formularza.text = "PCC-3"
    wariant_formularza = ET.SubElement(naglowek, "WariantFormularza")
    wariant_formularza.text = "6"
    cel_zlozenia = ET.SubElement(naglowek, "CelZlozenia", poz="P_6")
    cel_zlozenia.text = "1"
    data = ET.SubElement(naglowek, "Data", poz="P_4")
    data.text = "2024-07-29"
    kod_urzedu = ET.SubElement(naglowek, "KodUrzedu")
    kod_urzedu.text = "0271"

    # Podmiot1
    podmiot1 = ET.SubElement(deklaracja, "Podmiot1", rola="Podatnik")
    osoba_fizyczna = ET.SubElement(podmiot1, "OsobaFizyczna")
    pesel = ET.SubElement(osoba_fizyczna, "PESEL")
    pesel.text = data.get("PESEL")
    imie_pierwsze = ET.SubElement(osoba_fizyczna, "ImiePierwsze")
    imie_pierwsze.text = data.get("Imię")
    nazwisko = ET.SubElement(osoba_fizyczna, "Nazwisko")
    nazwisko.text = data.get("Nazwisko")
    data_urodzenia = ET.SubElement(osoba_fizyczna, "DataUrodzenia")
    data_urodzenia.text = data.get("Data urodzenia")

    # Adres zamieszkania
    if data["addres"]["type"] == "RAD":
        adres_zamieszkania = ET.SubElement(podmiot1, "AdresZamieszkaniaSiedziby", rodzajAdresu="RAD")
        adres_pol = ET.SubElement(adres_zamieszkania, "AdresPol")
        kraj = ET.SubElement(adres_pol, "KodKraju")
        kraj.text = data.get("Kraj")
        wojewodztwo = ET.SubElement(adres_pol, "Wojewodztwo")
        wojewodztwo.text = data.get("Województwo")
        powiat = ET.SubElement(adres_pol, "Powiat")
        powiat.text = data.get("Powiat")
        gmina = ET.SubElement(adres_pol, "Gmina")
        gmina.text = data.get("Gmina")
        ulica = ET.SubElement(adres_pol, "Ulica")
        ulica.text = data.get("Ulica")
        nr_domu = ET.SubElement(adres_pol, "NrDomu")
        nr_domu.text = data.get("Numer domu")
        nr_lokalu = ET.SubElement(adres_pol, "NrLokalu")
        nr_lokalu.text = data.get("Numer lokalu")
        miejscowosc = ET.SubElement(adres_pol, "Miejscowosc")
        miejscowosc.text = data.get("Miejscowość")
        kod_pocztowy = ET.SubElement(adres_pol, "KodPocztowy")
        kod_pocztowy.text = data.get("Kod pocztowy")
    else:
        adres_zamieszkania = ET.SubElement(podmiot1, "AdresZamieszkaniaSiedziby", rodzajAdresu="RAD")
        adres_pol = ET.SubElement(adres_zamieszkania, "AdresPol")
        kraj = ET.SubElement(adres_pol, "KodKraju")
        kraj.text = data.get("Kraj")
        wojewodztwo = ET.SubElement(adres_pol, "Wojewodztwo")
        wojewodztwo.text = data.get("Województwo")
        powiat = ET.SubElement(adres_pol, "Powiat")
        powiat.text = data.get("Powiat")
        gmina = ET.SubElement(adres_pol, "Gmina")
        gmina.text = data.get("Gmina")
        ulica = ET.SubElement(adres_pol, "Ulica")
        ulica.text = data.get("Ulica")
        nr_domu = ET.SubElement(adres_pol, "NrDomu")
        nr_domu.text = data.get("Numer domu")
        nr_lokalu = ET.SubElement(adres_pol, "NrLokalu")
        nr_lokalu.text = data.get("Numer lokalu")
        miejscowosc = ET.SubElement(adres_pol, "Miejscowosc")
        miejscowosc.text = data.get("Miejscowość")
        kod_pocztowy = ET.SubElement(adres_pol, "KodPocztowy")
        kod_pocztowy.text = data.get("Kod pocztowy")

    pozycje_szczegolowe = ET.SubElement(deklaracja, "PozycjeSzczegolowe")
    p_23 = ET.SubElement(pozycje_szczegolowe, "P_23")
    p_23.text = data.get("Treść i przedmiot czynności cywilnoprawnej")
    p_7 = ET.SubElement(pozycje_szczegolowe, "P_7")
    p_7.text = data.get("Rodzaj czynności cywilnoprawnej")
    p_24 = ET.SubElement(pozycje_szczegolowe, "P_24")
    p_24.text = data.get("Kwota czynności PLN")

    pouczenia = ET.SubElement(deklaracja, "Pouczenia")
    pouczenia.text = "1"

    tree = ET.ElementTree(deklaracja)
    ET.indent(tree, space="  ", level=0)  # Formatowanie XML
    tree.write("deklaracja.xml", encoding="UTF-8", xml_declaration=True)

data = {
    "Imię": "KAMIL",
    "Nazwisko": "WIRTUALNY",
    "PESEL": "54121832134",
    "NIP": "",
    "Data urodzenia": "1954-12-18",
    "Kraj": "PL",
    "Województwo": "ŚLĄSKIE",
    "Powiat": "M. KATOWICE",
    "Gmina": "M. KATOWICE",
    "Miejscowość": "KATOWICE",
    "Ulica": "ALPEJSKA",
    "Numer domu": "6",
    "Numer lokalu": "66",
    "Kod pocztowy": "66-666",
    "Treść i przedmiot czynności cywilnoprawnej": "Sprzedałem auto",
    "Rodzaj czynności cywilnoprawnej": "2",
    "Kwota czynności PLN": "10000"
}

generate_xml(data)
