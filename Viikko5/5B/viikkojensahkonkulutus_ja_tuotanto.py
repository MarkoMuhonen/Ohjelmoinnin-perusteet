"""
Python-ohjelma, joka:

Ohjelman tulee:

Lukea kaikki kolme CSV-tiedostoa: viikko41.csv, viikko42.csv, viikko43.csv.

Laskea jokaiselle viikolle (41, 42, 43) päiväkohtaiset summat:

viikonpäivä suomeksi (maanantai, tiistai, …)
päivän päivämäärä muodossa pv.kk.vuosi (esim. 13.10.2025)
kulutus vaiheittain 1–3 (kWh, 2 desimaalia, pilkku desimaalina)
tuotanto vaiheittain 1–3 (kWh, 2 desimaalia, pilkku desimaalina)
Kirjoittaa yhteenvedot tiedostoon yhteenveto.txt seuraavalla ajatuksella:

Raportissa on selkeä otsikko jokaiselle viikolle, esim.:
Viikon 41 sähkönkulutus ja -tuotanto (kWh, vaiheittain)
Päivä        Pvm         Kulutus [kWh]              Tuotanto [kWh]
                         v1      v2      v3         v1      v2      v3
---------------------------------------------------------------------------
maanantai    06.10.2025  12,35   1,56    2,78       0,01   0,39    0,52
tiistai      07.10.2025  ...
...
sunnuntai    12.10.2025  ...
Sama rakenne viikoille 42 ja 43 saman raportin sisällä.
Raportin lopussa saa olla esim. lyhyt yhteenveto kaikista viikoista (kokonaiskulutus ja -tuotanto), jos se helpottaa ohjelman rakentamista (tai teet sen bonus-ideana ⭐).
Tarkkaa tekstimuotoa ei ole betonoitu, mutta raportin tulee olla:

luettava ja looginen
selkeästi jäsennelty (otsikot, taulukkomaiset rivit, väliotsikot viikoille)



"""

from datetime import datetime, date
import sys





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

def selvita_viikko(paivat_datetime: list) -> int:
    # Palauttaa viikon numeron annetusta päivämäärälistasta
    # Oletetaan, että kaikki päivät ovat samalta viikolta
    ensimmäinen_paiva = paivat_datetime[0]
    return ensimmäinen_paiva.isocalendar()[1] 
     

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
    if len(sys.argv) < 2:
        print("Anna vähintään yksi tiedostonimi komentorivillä!")
        return
    for tiedosto in sys.argv[1:]:
        rivit = lue_data(tiedosto)
        print(tiedosto)
        
        # testikodia datan luvun tarkistamiseksi
        # tulosta_data(rivit)
        viikko = selvita_viikko(rivit[0])
        print("Viikon " + str(viikko) + "  sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")
        print("Päivä         Pvm           Kulutus [kWh]                 Tuotanto [kWh]")
        print("              (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
        print("-" * 80)
        for paiva in ["13.10.2025", "14.10.2025", "15.10.2025", "16.10.2025", "17.10.2025", "18.10.2025", "19.10.2025"]:
            paivanlukemat, viikonpaiva = paivantiedot(paiva, rivit)
            tulosta_yksittaiset_vaihelukemat(paiva, paivanlukemat, viikonpaiva)
        print("-" * 80)
        #print("Viikon " + str(viikko) + "  sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")

if __name__ == "__main__":
    main()