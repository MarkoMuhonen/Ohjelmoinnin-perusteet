"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funktioita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus):
    varausnumero = int(varaus[0])
    print(f"Varausnumero: {varausnumero}")
    
def hae_varaaja(varaus):
    nimi = varaus[1]
    print(f"Varaaja: {nimi}")

def hae_paiva(varaus):
    paiva = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    print(f"Päivämäärä: {paiva.strftime('%d.%m.%Y')}")

def hae_aloitusaika(varaus):
    aika = datetime.strptime(varaus[3], "%H:%M").time()
    print(f"Aloitusaika: {aika.strftime('%H.%M')}")

def hae_tuntimaara(varaus):
    tuntimaara = float(varaus[4])
    print(f"Tuntimäärä: {tuntimaara}")

def hae_tuntihinta(varaus):
    tuntihinta = float(varaus[5])
    print(f"Tuntihinta: {str(f'{tuntihinta:.2f}').replace('.', ',')} €")

def laske_kokonaishinta(varaus):
    tuntimaara = float(varaus[4])
    tuntihinta = float(varaus[5])
    kokonaishinta = tuntimaara * tuntihinta
    print(f"Kokonaishinta: {str(f'{kokonaishinta:.2f}').replace('.', ',')} €")

def hae_maksettu(varaus):
    maksettu = "Kyllä" if varaus[6] == "True" or varaus[6] == "1" else "Ei"
    print(f"Maksettu: {maksettu}")

def hae_kohde(varaus):
    print(f"Kohde: {varaus[7]}")

def hae_puhelin(varaus):
    print(f"Puhelin: {varaus[8]}")

def hae_sahkoposti(varaus):
    print(f"Sähköposti: {varaus[9]}")

def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto, luetaan ja splitataan sisalto
    with open(varaukset, "r", encoding="utf-8") as f:
        varaus = f.read().strip()
        varaus = varaus.split('|')

    # Toteuta loput funktio hae_varaaja(varaus) mukaisesti
    # Luotavat funktiota tekevat tietotyyppien muunnoksen
    # ja tulostavat esimerkkitulosteen mukaisesti

    hae_varausnumero(varaus)
    hae_varaaja(varaus)
    hae_paiva(varaus)
    hae_aloitusaika(varaus)
    hae_tuntimaara(varaus)
    hae_tuntihinta(varaus)
    laske_kokonaishinta(varaus)
    hae_maksettu(varaus)
    hae_kohde(varaus)
    hae_puhelin(varaus)
    hae_sahkoposti(varaus)

if __name__ == "__main__":
    main()