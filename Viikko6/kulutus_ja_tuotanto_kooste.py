# Copyright (c) 2025 Marko Muhonen
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

from datetime import datetime, date, timedelta  
from typing import Callable, Dict, List, Optional, Tuple

# Tyypit selkeyden ja testattavuuden vuoksi
Action = Callable[[], Optional[str]]  # Palauttaa seuraavan valikon nimen (tai None pysyäkseen samassa)
MenuOption = Tuple[str, Action]       # (kuvaus, toiminto)
Menu = Dict[str, MenuOption]          # näppäin -> (kuvaus, toiminto)
Menus = Dict[str, Menu]               # valikon nimi -> Menu

def safe_input(prompt: str, input_fn: Callable[[str], str]) -> str:
    """Kääre inputille, jotta voidaan injektoida testattava syötefunktio."""
    return input_fn(prompt)

def print_line(text: str, print_fn: Callable[[str], None]) -> None:
    """Kääre printille, jotta voidaan injektoida testattava tulostusfunktio."""
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


# --- Esimerkkisovellus alla --- #

# Tilaa ylläpitävä luokka (ei pakollinen, mutta siisti)
class AppState:
    def __init__(self) -> None:
        self.items: List[str] = []
        self.user: Optional[str] = None

state = AppState()

def header(title: str) -> str:
    # Esimerkki otsikon muotoilusta
    return f"\n--- {title.capitalize()} ---"

# Toiminnot (actions). Jokainen voi palauttaa seuraavan valikon nimen tai None.

def act_timerange_summary() -> Optional[str]:
    """Raportti 1: Päiväkohtainen yhteenveto aikaväliltä
    Kysy käyttäjältä:

    Alkupäivä: Anna alkupäivä (pv.kk.vvvv):
    Loppupäivä: Anna loppupäivä (pv.kk.vvvv):
    Raporttiin tulostetaan aikaväliltä:

    Alku- ja loppupäivä (pv.kk.vvvv-pv.kk.vvvv)
    Aikavälin kokonaiskulutus (kWh, 2 desimaalia, pilkku desimaalina)
    Aikavälin kokonaistuotanto (kWh, 2 desimaalia, pilkku desimaalina)
    Aikavälin keskilämpötila (esim. kaikkien tuntien lämpötilojen keskiarvo)
    """
    start_date_str = input("Anna aloituspäivämäärä (pv.kk.vvvv): ").strip()
    end_date_str = input("Anna lopetuspäivämäärä (pv.kk.vvvv): ").strip()
    try:
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
        end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
        if start_date > end_date:
            print("Aloituspäivämäärä ei voi olla lopetuspäivämäärää myöhempi.")
            return None
        print(f"Raportti aikaväliltä: {start_date} - {end_date}")
    except ValueError:
        print("Virheellinen päivämäärämuoto. Käytä muotoa pv.kk.vvvv.")
    return None



def act_monthly_summary() -> Optional[str]:
    print("Näytetään kuukausiyhteenveto (toiminto ei ole vielä toteutettu).")
    return None
def act_yearly_summary() -> Optional[str]:
    print("Näytetään aikavälin päiväyhteenveto (toiminto ei ole vielä toteutettu).")
    return None

def act_write_raport_to_file() -> Optional[str]:
    print("Kirjoitetaan raportti (toiminto ei ole vielä toteutettu).")
    return None

def act_go_print_to_file() -> str:
    # Siirtyminen toiseen valikkoon palauttamalla sen nimi
    return "tulosta_tiedostoon"

def act_go_filemenu() -> str:
    return "tulosta_tiedostoon"

def act_go_main() -> str:
    return "päävalikko"

def act_quit() -> str:
    print("Lopetetaan. Kiitos!")
    # Palautetaan tuntematon valikkonimi, jolloin run_menu lopettaa siististi, tai sitten ei
    quit()
    return "__exit__"

def main():    run_menu(
        start_menu="päävalikko",
        menus=menus,
        input_fn=input,
        print_fn=print,
        header_fn=header,
    )

# Valikkorakenne: yksi aliohjelma run_menu käsittelee kaikki
menus: Menus = {
    "päävalikko": {
        "1": ("Päiväkohtainen yhteenveto aikaväliltä", act_timerange_summary),
        "2": ("Kuukausikohtainen yhteenveto yhdelle kuukaudelle", act_monthly_summary),
        "3": ("Vuoden 2025 kokonaisyhteenveto", act_yearly_summary),
        "w": ("Tulosta tiedostoon", act_go_filemenu),
        "q": ("Lopeta", act_quit),
    },
    "tulosta_tiedostoon": {
        "1": ("Kirjoita raportti tiedostoon raportti.txt", act_write_raport_to_file),
        "m": ("Takaisin päävalikkoon", act_go_main),
        "q": ("Lopeta", act_quit),
        }
    }   

if __name__ == "__main__":
    main()
