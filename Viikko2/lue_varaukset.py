"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin. Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19.95 €
Kokonaishinta: 39.9 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""

from __future__ import annotations
from datetime import datetime

def main():
    # Määritellään tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan sisältö
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()

    # Tulostetaan varaus konsoliin
    #print(varaus)

    # Kokeile näitä
    #print(varaus.split('|'))


    
    varausId = varaus.split('|')[6]
    #print(varausId)
    #print(type(varausId))

    reservation = {
        "reservation_number": varausId[0],
        "user_name": varausId[1],
        "resource": varausId[2],
        "start": varausId[3],
        "end": varausId[4],
        "confirmed": True,
        "participants": 4   
    }

    print(f"Varausnumero: {reservation_number['resource']} klo {reservation['start'].strftime('%H:%M')}–{reservation['end'].strftime('%H:%M')}")

    """
    Edellisen olisi pitänyt tulostaa numeron 123, joka
    on oletuksena tekstiä.

    Voit kokeilla myös vaihtaa kohdan [0] esim. seuraavaksi [1]
    ja testata mikä muuttuu
    """

if __name__ == "__main__":
    main()