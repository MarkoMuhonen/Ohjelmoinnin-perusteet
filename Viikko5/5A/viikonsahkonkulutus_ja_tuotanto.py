"""
Python-ohjelma, joka:

1. Lukee tiedot tiedostosta viikko42.csv

2. Laskee jokaiselle viikonpäivälle (ma-su):

    - vaiheittaisen sähkönkulutuksen (vaihe 1-3) kWh-yksikössä
    - vaiheittaisen sähköntuotannon (vaihe 1-3) kWh-yksikössä

    - tulostaa tulokset konsoliin selkeänä, käyttäjäystävällisenä taulukkona.


Tiedosto sisältää viikon 42 (ma-su) tuntikohtaiset mittaukset:

- aika (päivämäärä ja kellonaika)
- kulutus kolmeen vaiheeseen jaettuna (Wh)
- tuotanto kolmeen vaiheeseen jaettuna (Wh)

Muunnetaan aineiston Wh → kWh ja esitetään tulokset kahden desimaalin tarkkuudella.

Tulostusrakenne:

Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)

Päivä         Pvm         Kulutus [kWh]                 Tuotanto [kWh]
             (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3
---------------------------------------------------------------------------
maanantai     13.10.2025   12,35   1,56    2,78          0,01   0,39   0,52
tiistai       14.10.2025   ...     ...     ...           ...    ...    ...
...
sunnuntai     19.10.2025   ...     ...     ...           ...    ...    ...

"""

from datetime import datetime




def muunna_rivitiedot(rivit: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 8 saraketta -> Lista -> Alkiot 0-6
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    
    return [
        #str(rivit[0]),
        datetime.strptime(rivit[0], "%Y-%m-%dT%H:%M:%S"),
        int(rivit[1]),
        int(rivit[2]),
        int(rivit[3]),
        int(rivit[4]),
        int(rivit[5])
    ]
            
     




def lue_data(datatiedosto: str) -> list:
    rivit = []
    with open(datatiedosto, "r", encoding="utf-8") as f:
        otsikkorivi = f.readline().strip().split(';')    # Ohitetaan otsikkorivi
    #    rivit.append(otsikkorivi)
        #print(otsikkorivi) #debuggia
        rivit.append(otsikkorivi)
        for rivi in f:
            rivi = rivi.strip()
            rivitiedot = rivi.split(';')    
            rivit.append(muunna_rivitiedot(rivitiedot))
    return rivit

def tulosta_rivit(rivit: list):
    #Tulostetaan datatiedoston rivit 
    print("Aikaleima              Kulutus_v1  Kulutus_v2  Kulutus_v3  Tuotanto_v1  Tuotanto_v2  Tuotanto_v3")
    print("-" * 80)
    for rivi in rivit[1:]:
        # rivi[0] on datetime, muut ovat int (Wh)
        aikaleima = rivi[0].strftime("%d.%m.%Y %H:%M")
        kulutus_v1 = f"{rivi[1]/1000:.2f}".replace('.', ',')
        kulutus_v2 = f"{rivi[2]/1000:.2f}".replace('.', ',')
        kulutus_v3 = f"{rivi[3]/1000:.2f}".replace('.', ',')
        tuotanto_v1 = f"{rivi[4]/1000:.2f}".replace('.', ',')
        tuotanto_v2 = f"{rivi[5]/1000:.2f}".replace('.', ',')
        # Jos on myös tuotanto_v3, lisää se
        # tuotanto_v3 = f"{rivi[6]/1000:.2f}".replace('.', ',')
        print(f"{aikaleima:20} {kulutus_v1:10} {kulutus_v2:10} {kulutus_v3:10} {tuotanto_v1:12} {tuotanto_v2:12}")
    




    return


def main():
    rivit = lue_data("viikko42.csv")
    tulosta_rivit(rivit)
    #print(" | ".join(rivit[0]))
    #print("------------------------------------------------------------------------")
    #for varaus in varaukset[1:]:
    #    print(" | ".join(str(x) for x in varaus))
    #    tietotyypit = [type(x).__name__ for x in varaus]
    #    print(" | ".join(tietotyypit))
    #    print("------------------------------------------------------------------------")

if __name__ == "__main__":
    main()