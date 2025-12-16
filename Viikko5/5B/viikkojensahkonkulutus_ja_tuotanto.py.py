from datetime import datetime, date
import sys


def selvita_paiva(aikaleima: datetime) -> str:
    """
    Palauttaa viikonpäivän nimen suomeksi annetusta aikaleimasta.

    :param aikaleima: datetime-olio
    :return: viikonpäivän nimi suomeksi (esim. 'maanantai')
    """
    viikonpaivat = {
        0: "maanantai",
        1: "tiistai",
        2: "keskiviikko",
        3: "torstai",
        4: "perjantai",
        5: "lauantai",
        6: "sunnuntai"
    }
    return str(viikonpaivat[aikaleima.weekday()])   


def selvita_viikko(paivat_datetime: list) -> int:
    """
    Palauttaa viikon numeron annetusta päivämäärälistasta.
    Oletetaan, että kaikki päivät ovat samalta viikolta.

    :param paivat_datetime: lista datetime.date-olioita
    :return: viikon numero (int)
    """
    ensimmäinen_paiva = paivat_datetime[0]
    return int(ensimmäinen_paiva.isocalendar()[1])   


def paivantiedot(paiva: str, lukemat: list) -> tuple[list, str]:
    """
    Laskee annetun päivän kulutus- ja tuotantosummat vaiheittain sekä palauttaa viikonpäivän nimen.

    :param paiva: päivämäärä merkkijonona (pv.kk.vvvv)
    :param lukemat: lista mittausrivejä (lista, jossa jokainen alkio on lista)
    :return: tuple (lasketutTiedot-lista, viikonpäivän nimi)
    """
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
        # Käydään läpi kaikki rivit ja summataan, jos päivämäärä täsmää
        if lukema[0].date() == date(vuosi, kk, pv):
            kulutus1vaihe += lukema[1]
            kulutus2vaihe += lukema[2]
            kulutus3vaihe += lukema[3]
            tuotanto1vaihe += lukema[4]
            tuotanto2vaihe += lukema[5]
            tuotanto3vaihe += lukema[6]
    # Muutetaan Wh → kWh ja lisätään listaan
    lasketutTiedot.append(kulutus1vaihe/1000)
    lasketutTiedot.append(kulutus2vaihe/1000)
    lasketutTiedot.append(kulutus3vaihe/1000)
    lasketutTiedot.append(tuotanto1vaihe/1000)
    lasketutTiedot.append(tuotanto2vaihe/1000)
    lasketutTiedot.append(tuotanto3vaihe/1000)
    return tuple(lasketutTiedot), str(viikonpaiva)


def kaikkitiedot(lukemat: list) -> list:
    """
    Laskee kaikkien annettujen lukemien kokonaiskulutuksen ja -tuotannon vaiheittain.

    :param lukemat: lista mittausrivejä (lista, jossa jokainen alkio on lista)
    :return: lista kokonaiskulutuksista ja -tuotannoista vaiheittain (kWh)
    """
    koontikulutus1vaihe = 0
    koontikulutus2vaihe = 0
    koontikulutus3vaihe = 0
    koontituotanto1vaihe = 0
    koontituotanto2vaihe = 0
    koontituotanto3vaihe = 0
    for lukema in lukemat:
        koontikulutus1vaihe += lukema[1]
        koontikulutus2vaihe += lukema[2]
        koontikulutus3vaihe += lukema[3]
        koontituotanto1vaihe += lukema[4]
        koontituotanto2vaihe += lukema[5]
        koontituotanto3vaihe += lukema[6]
    koontiTiedot = [
        koontikulutus1vaihe/1000,
        koontikulutus2vaihe/1000,
        koontikulutus3vaihe/1000,
        koontituotanto1vaihe/1000,
        koontituotanto2vaihe/1000,
        koontituotanto3vaihe/1000
    ]
    return list(koontiTiedot) 



def lue_data(datatiedosto: str) -> list:
    """
    Lukee annetun CSV-tiedoston ja palauttaa rivit listana, jossa jokainen rivi on muunnettu oikeisiin tietotyyppeihin.

    :param datatiedosto: tiedostonimi (str)
    :return: lista riveistä, joissa jokainen rivi on lista oikeissa tietotyypeissä
    """
    rivit = []
    with open(datatiedosto, "r", encoding="utf-8") as f:
        otsikkorivi = f.readline() # Ohitetaan otsikkorivi
        for rivi in f:
            rivi = rivi.strip()
            rivitiedot = rivi.split(';')    
            rivit.append(muunna_rivitiedot(rivitiedot))
    return list(rivit)        


def muunna_rivitiedot(rivit: list) -> list:
    """
    Muuntaa yhden tiedostorivin tiedot oikeisiin tietotyyppeihin (datetime, float).

    :param rivit: lista merkkijonoja (yksi tiedostorivi pilkottuna)
    :return: lista, jossa tiedot oikeissa tietotyypeissä
    """
    return [
        datetime.strptime(rivit[0], "%Y-%m-%dT%H:%M:%S"),
        float(rivit[1]),
        float(rivit[2]),
        float(rivit[3]),
        float(rivit[4]),
        float(rivit[5]),
        float(rivit[6])
    ]


def tulosta_yksittaiset_vaihelukemat(paivamaara:str, paivanlukemat: list, viikonpaiva: str):
    """
    Tulostaa yhden päivän kulutus- ja tuotantolukemat vaiheittain taulukkomuodossa.

    :param paivamaara: päivämäärä merkkijonona (pv.kk.vvvv)
    :param paivanlukemat: lista päivän kulutus- ja tuotantolukemista (kWh)
    :param viikonpaiva: viikonpäivän nimi suomeksi
    """
    print(f"{viikonpaiva.capitalize():11}", end= "   ")
    print(f"{paivamaara:<12}",  end= "  ")
    print(f"{paivanlukemat[0]:>6.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[1]:>6.2f}".replace('.', ','), end= " ") 
    print(f"{paivanlukemat[2]:>6.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[3]:>14.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[4]:>6.2f}".replace('.', ','), end= " ")
    print(f"{paivanlukemat[5]:>6.2f}".replace('.', ','), end= " ")
    print()
    return


def tulosta_raportti(tiedosto: str):
    """
    Tulostaa yhden tiedoston (viikon) raportin päiväkohtaisesti taulukkomuodossa.

    :param tiedosto: tiedostonimi (str)
    """
    rivit = lue_data(tiedosto)
    viikko = selvita_viikko([rivi[0].date() for rivi in rivit])
    print("Viikon " + str(viikko) + " sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")
    print("Päivä         Pvm           Kulutus [kWh]                 Tuotanto [kWh]")
    print("              (pv.kk.vvvv)  v1      v2      v3            v1     v2     v3")
    print("-" * 80)
    paivamaarat = sorted({rivi[0].date() for rivi in rivit})
    for paiva in paivamaarat:
        paiva_str = paiva.strftime("%d.%m.%Y")
        paivanlukemat, viikonpaiva = paivantiedot(paiva_str, rivit)
        tulosta_yksittaiset_vaihelukemat(paiva_str, paivanlukemat, viikonpaiva)
    print("-" * 80)
    print()
    return


def tulosta_yhteenveto(koontiLukemat: list):
    """
    Tulostaa kaikkien tiedostojen (viikkojen) yhteenvedon kulutuksesta ja tuotannosta vaiheittain.

    :param koontiLukemat: lista kokonaiskulutuksista ja -tuotannoista vaiheittain (kWh)
    """
    print("\n\nKoonti kaikilta annetuilta viikoilta - sähkönkulutus ja -tuotanto (kWh, vaiheittain)", end="\n\n")
    print("       Kulutus [kWh]                   Tuotanto [kWh]")
    print("  v1        v2        v3            v1        v2        v3")
    print("-" * 80)
    print(f"{koontiLukemat[0]:>7.2f}".replace('.', ','), end=" ")
    print(f"{koontiLukemat[1]:>8.2f}".replace('.', ','), end=" ")
    print(f"{koontiLukemat[2]:>8.2f}".replace('.', ','), end=" ")
    print(f"{koontiLukemat[3]:>14.2f}".replace('.', ','), end=" ")
    print(f"{koontiLukemat[4]:>9.2f}".replace('.', ','), end=" ")
    print(f"{koontiLukemat[5]:>9.2f}".replace('.', ','))
    print("-" * 80)
    return


def main():
    """
    Pääohjelma: lukee tiedostot, tulostaa raportit ja yhteenvedon sekä ruudulle että tiedostoon.
    """
    if len(sys.argv) < 2:
        print("Anna vähintään yksi tiedostonimi komentorivillä!")
        return

    kaikki_rivit = []
    for tiedosto in sys.argv[1:]:
        tulosta_raportti(tiedosto)
        rivit = lue_data(tiedosto)
        kaikki_rivit.extend(rivit)

    koontiLukemat = kaikkitiedot(kaikki_rivit)
    tulosta_yhteenveto(koontiLukemat)
    print()

    # Tulostetaan sama raportti myös tiedostoon
    # Ohjataan tulostus tiedostoon, ja käytetään samoja tulostusfunktioita
    with open("yhteenveto.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        for tiedosto in sys.argv[1:]:
            tulosta_raportti(tiedosto)
        tulosta_yhteenveto(koontiLukemat)
        print()
        sys.stdout = sys.__stdout__
                   
if __name__ == "__main__":
    main()