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

from datetime import datetime, date


def muunna_rivitiedot(rivit: list) -> list:
    # muunnetaan rivitiedot oikeisiin tietotyyppeihin
    # rivillä on 7 saraketta -> Lista -> Alkiot 0-6
    
    return [
        datetime.strptime(rivit[0], "%Y-%m-%dT%H:%M:%S"),
        float(rivit[1]),
        float(rivit[2]),
        float(rivit[3]),
        float(rivit[4]),
        float(rivit[5]),
        float(rivit[6])
    ]


def selvita_paiva(aikaleima: datetime) -> str:
    # Palauttaa viikonpäivän nimen suomeksi annetusta aikaleimasta
    
    viikonpaivat = {
        0: "maanantai",
        1: "tiistai",
        2: "keskiviikko",
        3: "torstai",
        4: "perjantai",
        5: "lauantai",
        6: "sunnuntai"
    }
    return viikonpaivat[aikaleima.weekday()]        
     

def paivantiedot(paiva: str, lukemat: list) -> tuple[list, str]:
    paiva_datetime = datetime.strptime(paiva, "%d.%m.%Y").date()
    viikonpaiva = selvita_paiva(paiva_datetime)
    pv = int(paiva.split('.')[0])
    kk = int(paiva.split('.')[1])
    vuosi = int(paiva.split('.')[2])
    lasketutTiedot = []
    kulutus1vaihe = 0
    kulutus2vaihe = 0
    kulutus3vaihe = 0
    tuotanto1vaihe = 0
    tuotanto2vaihe = 0
    tuotanto3vaihe = 0
    for lukema in lukemat:
        #print(lukema[0].date())
        if lukema[0].date() == date(vuosi, kk, pv):
            kulutus1vaihe += lukema[1]
            kulutus2vaihe += lukema[2]
            kulutus3vaihe += lukema[3]
            tuotanto1vaihe += lukema[4]
            tuotanto2vaihe += lukema[5]
            tuotanto3vaihe += lukema[6]
    
    lasketutTiedot.append(kulutus1vaihe/1000)
    lasketutTiedot.append(kulutus2vaihe/1000)
    lasketutTiedot.append(kulutus3vaihe/1000)
    lasketutTiedot.append(tuotanto1vaihe/1000)
    lasketutTiedot.append(tuotanto2vaihe/1000)
    lasketutTiedot.append(tuotanto3vaihe/1000)
    return lasketutTiedot, viikonpaiva
   

def lue_data(datatiedosto: str) -> list:
    rivit = []
    with open(datatiedosto, "r", encoding="utf-8") as f:
        otsikkorivi = f.readline() # Ohitetaan otsikkorivi
        for rivi in f:
            rivi = rivi.strip()
            rivitiedot = rivi.split(';')    
            rivit.append(muunna_rivitiedot(rivitiedot))
    return rivit

def tulosta_data(rivit: list):
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
        tuotanto_v3 = f"{rivi[6]/1000:.2f}".replace('.', ',')
        print(f"{aikaleima:20} {kulutus_v1:10} {kulutus_v2:10} {kulutus_v3:10} {tuotanto_v1:12} {tuotanto_v2:12}")
    
    return

def tulosta_yksittaiset_vaihelukemat(paiva:str, paivanlukemat: list, viikonpaiva: str):
    #for lukema in paivanlukemat:
    print(f"{viikonpaiva.capitalize():11}", end= "   ")
    print(f"{paiva:<12}",  end= "  ")
    print(f"{paivanlukemat[0]:>6.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[1]:>6.2f}".replace('.', ','), end= " ") 
    print(f"{paivanlukemat[2]:>6.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[3]:>14.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[4]:>6.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[5]:>6.2f}".replace('.', ','), end= " ")
    print()
    return

def main():
    rivit = lue_data("viikko42.csv")
    # testikodia datan luvun tarkistamiseksi
    # tulosta_data(rivit)
    print("Viikon 42 sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")
    print("Päivä         Pvm           Kulutus [kWh]                 Tuotanto [kWh]")
    print("              (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    print("-" * 80)
    for paiva in ["13.10.2025", "14.10.2025", "15.10.2025", "16.10.2025", "17.10.2025", "18.10.2025", "19.10.2025"]:
        paivanlukemat, viikonpaiva = paivantiedot(paiva, rivit)
        tulosta_yksittaiset_vaihelukemat(paiva, paivanlukemat, viikonpaiva)
   
   

if __name__ == "__main__":
    main()