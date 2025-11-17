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
    #print(varaus)  # tulostaa koko rivin tiedostosta

    # Kokeile näitä
    #print(varaus.split('|')) # Jakaa merkkijonon osiin erotinmerkin '|' kohdalta ja tulostaa listana

    
    varausId = varaus.split('|') # Jaetaan merkkijono osiin erotinmerkin '|' kohdalta
    
    
    reservation = {
        "reservation_number": int(varausId[0]),
        "user_name": varausId[1],
        "reservation_date": varausId[2],
        "start_time": varausId[3],
        "duration": float(varausId[4]),
        "hourly_rate": float(varausId[5]),
        "total_price": float(varausId[4]) * float(varausId[5]),
        "paid": bool(varausId[6]),
        "location": varausId[7],
        "phone": varausId[8],
        "email": varausId[9]      
    }

    paiva = datetime.strptime(reservation['reservation_date'], "%Y-%m-%d").date()
    suomalainenPaiva = paiva.strftime("%d.%m.%Y")
    aika = datetime.strptime(reservation['start_time'], "%H:%M").time()
    suomalainenAika = aika.strftime("%H.%M")
    #print(f"Muunnettu päivämäärä: {suomalainenPaiva}") #testitulostus
    #print(f"Muunnettu aika: {suomalainenAika}") #testitulostus
          

    print()
    print(f"Varausnumero: {reservation['reservation_number']}")
    print(f"Varaaja: {reservation['user_name']}")
    print(f"Päivämäärä: {suomalainenPaiva}")
    print(f"Aloitusaika: {suomalainenAika}")
    print(f"Tuntimäärä: {reservation['duration']}")
    print(f"Tuntihinta: {reservation['hourly_rate']} €")
    print(f"Kokonaishinta: {reservation['total_price']} €")
    print(f"Maksettu: {reservation['paid']}")
    print(f"Kohde: {reservation['location']}")
    print(f"Puhelin: {reservation['phone']}")
    print(f"Sähköposti: {reservation['email']}")
 


if __name__ == "__main__":
    main()