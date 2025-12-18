# Copyright (c) 2025 Ville Heikkiniemi
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
def act_set_user() -> Optional[str]:
    name = input("Anna käyttäjän nimi: ").strip()
    if not name:
        print("Nimi ei voi olla tyhjä.")
        return None
    state.user = name
    print(f"Käyttäjä asetettu: {state.user}")
    return None  # Pysy samassa valikossa

def act_add_item() -> Optional[str]:
    item = input("Lisättävä kohde: ").strip()
    if not item:
        print("Kohde ei voi olla tyhjä.")
        return None
    state.items.append(item)
    print(f"Lisätty: {item}")
    return None

def act_list_items() -> Optional[str]:
    if not state.items:
        print("Ei kohteita.")
    else:
        print("Kohteet:")
        for i, it in enumerate(state.items, start=1):
            print(f"  {i}. {it}")
    return None

def act_clear_items() -> Optional[str]:
    confirm = input("Tyhjennetään kaikki kohteet? (k/e): ").strip().lower()
    if confirm == "k":
        state.items.clear()
        print("Kohteet tyhjennetty.")
    else:
        print("Peruutettu.")
    return None

def act_go_settings() -> str:
    # Siirtyminen toiseen valikkoon palauttamalla sen nimi
    return "asetukset"

def act_go_file() -> str:
    return "tiedostoon"

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
        "1": ("Aikavälin päiväyhteenveto", act_set_user),
        "2": ("Kuukausiyhteenveto", act_add_item),
        "3": ("Vuosiyhteenveto", act_list_items),
        "4": ("joku muu", act_clear_items),
        "s": ("Siirry asetuksiin", act_go_settings),
        "q": ("Lopeta", act_quit),
    },
    "asetukset": {
        "1": ("Näytä nykyinen käyttäjä", lambda: (print(f"Nykyinen käyttäjä: {state.user or '-'}") or None)),
        "2": ("Vaihda käyttäjä", act_set_user),
        "m": ("Takaisin päävalikkoon", act_go_main),
        "q": ("Lopeta", act_quit),
    }
    # "__exit__" ei ole varsinaisesti menu, mutta exit-polku
}

if __name__ == "__main__":
    main()
