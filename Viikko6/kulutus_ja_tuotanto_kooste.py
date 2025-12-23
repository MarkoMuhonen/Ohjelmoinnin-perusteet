# Copyright (c) 2025 Marko Muhonen
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

# Ohjelma, joka lukee Elenian .csv raporttitiedoston,
# ja tulostaa kulutus- ja tuotantotiedot vaiheittain
#
# Käytettävä csv-tiedosto (tiedostot) annetaan komentoriviparametrina.
# Ohjelma tukee useamman tiedoston käsittelyä peräkkäin,
# ja tulostaa yhteenvedon kaikista tiedostoista.
# Vuosi 2025 on lukittu koodissa, päiväkohtainen aikavälilaskelma toimii pidemmälläkin aikajaksolla.
#


from datetime import datetime, date, timedelta  
from typing import Callable, Dict, List, Optional, Tuple
import sys

# Tyypit selkeyden ja testattavuuden vuoksi
Action = Callable[[], Optional[str]]  # Palauttaa seuraavan valikon nimen (tai None pysyäkseen samassa)
MenuOption = Tuple[str, Action]       # (kuvaus, toiminto)
Menu = Dict[str, MenuOption]          # näppäin -> (kuvaus, toiminto)
Menus = Dict[str, Menu]               # valikon nimi -> Menu

def safe_input(prompt: str, input_fn: Callable[[str], str]) -> str:
    """
    Kääre inputille, jotta voidaan injektoida testattava syötefunktio.

    :param prompt: Käyttäjälle näytettävä syötekehotus
    :param input_fn: Syötefunktio (esim. input)
    :return: Käyttäjän syöte merkkijonona
    """
    return input_fn(prompt)

def print_line(text: str, print_fn: Callable[[str], None]) -> None:
    """
    Kääre printille, jotta voidaan injektoida testattava tulostusfunktio.

    :param text: Tulostettava teksti
    :param print_fn: Tulostusfunktio (esim. print)
    """
    print_fn(text)

def run_menu(
    start_menu: str,
    menus: Menus,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[[str], None] = print,
    header_fn: Optional[Callable[[str], str]] = None,
) -> None:
    """
    Yksi aliohjelma, joka hoitaa useamman valikon näyttämisen ja navigoinnin.

    - start_menu: aloitusvalikon nimi
    - menus: sanakirja (valikon nimi -> valikkorakenne)
    - input_fn / print_fn: injektoitavat IO-funktiot (helpottaa testausta)
    - header_fn: valikon otsikon generointi (esim. tehosteet)
    """
    current_menu = start_menu
    while True:
        if current_menu == "__exit__":
            return
       
        if current_menu not in menus:
            print_line(f"Virhe: tuntematon valikko '{current_menu}'. Lopetetaan.", print_fn)
            return

        menu = menus[current_menu]

        # Tulosta otsikko
        if header_fn:
            print_line(header_fn(current_menu), print_fn)
        else:
            print_line(f"\n=== {current_menu.upper()} ===", print_fn)

        # Tulosta kaikki vaihtoehdot järjestyksessä näppäimen mukaan
        for key, (label, _) in menu.items():
            print_line(f"[{key}] {label}", print_fn)

        choice = safe_input("Valinta: ", input_fn).strip()

        if choice in menu:
            label, action = menu[choice]
            try:
                # Suorita toiminto; se voi palauttaa seuraavan valikon nimen
                next_menu = action()
            except Exception as ex:
                print_line(f"Toiminnon aikana tapahtui virhe: {ex}", print_fn)
                next_menu = None

            # Jos toiminto määrittää seuraavan valikon, siirry siihen
            if isinstance(next_menu, str):
                current_menu = next_menu
            else:
                # Muuten pysytään samassa valikossa
                continue
        else:
            print_line("Virheellinen valinta. Yritä uudelleen.", print_fn)


# Tilaa ylläpitävä luokka 
class AppState:
    """
    Luokka, joka ylläpitää sovelluksen tilaa (mm. käyttäjä, rivit, raportti).

    Attributes:
        rivit (dict): luettu cscv-data sanakirjana
        report (str): Viimeisin luotu raportti merkkijonona
    """
    def __init__(self) -> None:
        self.rivit: dict = {}
        self.report: str = ""

state = AppState()

def header(title: str) -> str:
    """
    Muotoilee valikon otsikon.

    :param title: Otsikon teksti
    :return: Muotoiltu otsikko merkkijonona
    """
    return f"\n--- {title.capitalize()} ---"

def muunna_rivitiedot(rivit: list) -> dict:
    """
    Muuntaa yhden tiedostorivin tiedot oikeisiin tietotyyppeihin (datetime, float).

    :param rivit: lista merkkijonoja (yksi tiedostorivi pilkottuna)
    :return: sanakirja, jossa tiedot oikeissa tietotyypeissä
    """
    return {
        'dateiso': datetime.fromisoformat(rivit[0]),
        'consumption': float(rivit[1].replace(',', '.')),
        'production': float(rivit[2].replace(',', '.')),
        'temperature': float(rivit[3].replace(',', '.'))       
        }



def lue_data(datatiedosto: str) -> dict:
    """
    Lukee annetun CSV-tiedoston ja palauttaa rivit sanakirjana, jossa jokainen rivi on muunnettu oikeisiin tietotyyppeihin.

    :param datatiedosto: tiedostonimi (str)
    :return: sanakirja, jossa avaimena aikaleima ja arvona mittaustiedot
    """
    rivit = {}
    with open(datatiedosto, "r", encoding="utf-8") as f:
        otsikkorivi = f.readline() # Ohitetaan otsikkorivi
        ohitus = False
        for rivi in f:
            rivi = rivi.strip()
            rivitiedot = rivi.split(';')
            if len(rivitiedot) < 4 and ohitus == False:
                print(f"Datassa liian vähän kenttiä, tuotanto puuttuu? korvataan tuotantoluvut nollilla.")
                ohitus = True
            if len(rivitiedot) == 3:
                rivitiedot.insert(2, "0.0")
            
            data = muunna_rivitiedot(rivitiedot)
            rivit[data['dateiso']] = { 
                'consumption': data['consumption'],
                'production': data['production'],
                'temperature': data['temperature']
            }
    return rivit        


# Toiminnot (actions). Jokainen voi palauttaa seuraavan valikon nimen tai None.

def act_timerange_summary() -> Optional[str]:
    """
    Raportti 1: Päiväkohtainen yhteenveto aikaväliltä
    Kysyy käyttäjältä alkupäivän ja loppupäivän, ja tulostaa aikavälin kulutuksen, tuotannon ja keskilämpötilan.

    :return: None
    """
    start_date_str = input("Anna aloituspäivämäärä (pv.kk.vvvv): ").strip()
    end_date_str = input("Anna lopetuspäivämäärä (pv.kk.vvvv): ").strip()
    try:
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
        end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
        if start_date > end_date:
            print("Aloituspäivämäärä ei voi olla lopetuspäivämäärää myöhempi.")
            return None
        report = "\n"
        report += "-" * 80 + "\n"
        report += f"Raportti aikaväliltä: {start_date.day}.{start_date.month}.{start_date.year} - {end_date.day}.{end_date.month}.{end_date.year}\n"
        report += "-" * 80 + "\n"
        report += f"Aikavälin kokonaiskulutus:  {calculate_total_consumption_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " kWh\n"
        report += f"Aikavälin kokonaistuotanto: {calculate_total_production_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " kWh\n"
        report += f"Aikavälin keskilämpötila:   {calculate_average_temperature_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " °C\n"
        report += "-" * 80 + "\n"
        state.report = report
        print(report)
    except ValueError:
        print("\nVirheellinen päivämäärämuoto. Käytä muotoa pv.kk.vvvv.")
    return None


def calculate_total_consumption_for_timerange(
        start_date: date,
        end_date: date,
        rivit: dict
    ) -> float:
    """
    Laskee ja palauttaa aikavälin kokonaiskulutuksen (kWh).
    Tätä toimintoa käytetään kaikkien raporttien 1, 2 ja 3 yhteydessä.

    :param start_date: aikavälin alkupäivä
    :param end_date: aikavälin loppupäivä
    :param rivit: mittaustietosanakirja
    :return: kokonaiskulutus (float)
    """
    total = 0.0
    for aikaleima, data in rivit.items():
        if start_date <=aikaleima.date() <= end_date: 
            total += data['consumption']
    return float(total) 


def calculate_total_production_for_timerange(
        start_date: date,
        end_date: date,
        rivit: dict
    ) -> float:
    """
    Laskee ja palauttaa aikavälin kokonaistuotannon (kWh).
    Tätä toimintoa käytetään kaikkien raporttien 1, 2 ja 3 yhteydessä.
    
    :param start_date: aikavälin alkupäivä
    :param end_date: aikavälin loppupäivä
    :param rivit: mittaustietosanakirja
    :return: kokonaistuotanto (float)
    """
    total = 0.0
    for aikaleima, data in rivit.items():
        if start_date <=aikaleima.date() <= end_date: 
            total += data['production']
    return float(total) 


def calculate_average_temperature_for_timerange(
        start_date: date,
        end_date: date,
        rivit: dict
    ) -> float:
    """
    Laskee ja palauttaa aikavälin keskilämpötilan.
    Tätä toimintoa käytetään kaikkien raporttien 1, 2 ja 3 yhteydessä.
    
    :param start_date: aikavälin alkupäivä
    :param end_date: aikavälin loppupäivä
    :param rivit: mittaustietosanakirja
    :return: keskilämpötila (float)
    """
    total = 0.0
    measurements_count = 0
    for aikaleima, data in rivit.items():
        if start_date <=aikaleima.date() <= end_date: 
            total += data['temperature']
            measurements_count += 1

    average = total / measurements_count if measurements_count > 0 else 0.0
    return float(average)


def act_monthly_summary() -> Optional[str]:
    """
    Raportti 2: Kuukausikohtainen yhteenveto.
    Kysyy käyttäjältä kuukauden numeron ja tulostaa kuukauden kulutuksen, tuotannon ja keskilämpötilan.

    :return: None
    """
    month_nr = input("Anna kuukauden numero (1–12): ").strip()
    
    try:
        month_nr = int(month_nr)
        if month_nr <1 or month_nr >12:
            print("Anna kuukausi numeroilla väliltä 1–12.")
            return None
        month_in_text = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu",
                         "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
        year = next(iter(state.rivit)).year if state.rivit else datetime.now().year
        start_date, end_date = get_month_range(year, month_nr)
      
        report = "\n"
        report += "-" * 80 + "\n"
        report += f"Raportti : {month_in_text[month_nr -1] } {year}\n"
        report += "-" * 80 + "\n"
        report += f"Kuukauden kokonaiskulutus:  {calculate_total_consumption_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " kWh\n"
        report += f"Kuukauden kokonaistuotanto: {calculate_total_production_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " kWh\n"
        report += f"Kuukauden keskilämpötila:   {calculate_average_temperature_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " °C\n"
        report += "-" * 80 + "\n"
        state.report = report
        print(report)
    except ValueError:
        print("Virheellinen kuukauden numero. Anna kuukausi numeroilla väliltä 1–12.")
    return None

def act_yearly_summary() -> Optional[str]:
    """
    Raportti 3: Vuosikohtainen yhteenveto.
    Tulostaa vuoden kulutuksen, tuotannon ja keskilämpötilan.
    (lukee vuoden automaattisesti datasta ensimmäisen aikaleiman perusteella)

    :return: None
    """
           
    try:
        year = next(iter(state.rivit)).year if state.rivit else datetime.now().year
        start_date, end_date = get_year_range(year)
      
        report = "\n"
        report += "-" * 80 + "\n"
        report += f"Raportti vuodelta {year}\n"
        report += "-" * 80 + "\n"
        report += f"Koko vuoden kokonaiskulutus:  {calculate_total_consumption_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " kWh\n"
        report += f"Koko vuoden kokonaistuotanto: {calculate_total_production_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " kWh\n"
        report += f"Koko vuoden keskilämpötila:   {calculate_average_temperature_for_timerange(start_date, end_date, state.rivit):>8.2f}".replace('.', ',') + " °C\n"
        report += "-" * 80 + "\n"
        state.report = report
        print(report)
    except ValueError:
        print("Virheellinen kuukauden numero. Anna kuukausi numeroilla väliltä 1–12.")
    return None

def get_month_range(year: int, month: int) -> tuple[date, date]:
    """
    Palauttaa annetun vuoden perusteella kuukauden ensimmäisen ja viimeisen päivän.
    
    :param year: vuosi
    :param month: kuukausi
    :return: (alkupäivä, loppupäivä)
    """
    start_date = date(year, month, 1)
    # To get the last day, go to the first day of the next month and subtract one day
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)
    return start_date, end_date

def get_year_range(year: int) -> tuple[date, date]:
    """
    Palauttaa vuoden ensimmäisen ja viimeisen päivän.

    :param year: vuosi
    :return: (alkupäivä, loppupäivä)
    """
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    return start_date, end_date
    
def act_write_report_to_file(report: str) -> Optional[str]:
    """
    Kirjoittaa annetun raportin tiedostoon raportti.txt.

    :param report: raportin sisältö merkkijonona
    :return: None
    """
    if not report:
        print("Ei raporttia kirjoitettavaksi. Luo raportti ensin.")
        return None
    with open("raportti.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print("\nRaportti kirjoitettu tiedostoon raportti.txt")
    return None
    
def act_go_filemenu() -> str:
    """
    Siirtyy tulostusvalikkoon.
    :return: seuraavan valikon nimi
    """
    return "tulosta_tiedostoon"

def act_go_main() -> str:
    """
    Siirtyy päävalikkoon.
    :return: seuraavan valikon nimi
    """
    return "päävalikko"

def act_quit() -> str:
    """
    Lopettaa ohjelman.
    :return: "__exit__" (ohjelman lopetus)
    """
    print("Lopetetaan. Kiitos!")
    return "__exit__"


"""
Valikkorakenne sanakirjalla: yksi aliohjelma run_menu käsittelee kaikki
- ensimmäinen kenttä on näppäin, toinen kenttä on kuvaus, ja viimeinen kenttä on toiminto (action)
"""  

menus: Menus = {
    "päävalikko": {
        "1": ("Päiväkohtainen yhteenveto aikaväliltä", act_timerange_summary),
        "2": ("Kuukausikohtainen yhteenveto yhdelle kuukaudelle", act_monthly_summary),
        "3": ("Vuoden 2025 kokonaisyhteenveto", act_yearly_summary),
        "w": ("Tulosta tiedostoon -valikko", act_go_filemenu),
        "q": ("Lopeta", act_quit),
    },
    "tulosta_tiedostoon": {
        "1": ("Kirjoita raportti tiedostoon raportti.txt", lambda: act_write_report_to_file(state.report)) or "päävalikko",
        "m": ("Takaisin päävalikkoon", act_go_main),
        "q": ("Lopeta", act_quit),
        }
    }   

def main():    
    """
    Pääohjelma: lukee parametrina annetun tiedoston (tiedostot), kerää datan ja käynnistää valikkosilmukan.
    Ohjelma tukee useamman tiedoston käsittelyä peräkkäin, ja yhdistää datan yhdeksi kokonaisuudeksi, mutta 
    kuukausiraportti ja vuosiraportti lasketaan aina ensimmäisen tiedoston datasta.
    """
    
    if len(sys.argv) < 2:
        print("Anna parametrinä vähintään yksi Elenian .csv raporttitiedosto komentorivillä!")
        return
 
    for file in sys.argv[1:]:
        rivit = lue_data(file)
        state.rivit.update(rivit)
           
    run_menu(
        start_menu="päävalikko",
        menus=menus,
        input_fn=input,
        print_fn=print,
        header_fn=header,
    )


if __name__ == "__main__":
    main()
