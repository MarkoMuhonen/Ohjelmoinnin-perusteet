"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int |           str     |           str             |     str    |     date   |   time   |int| float | bool |      str    | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30:00 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45:00 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15:00 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    # Tähän tulee siis varaus oletustietotyypeillä (str)
    # Varauksessa on 11 saraketta -> Lista -> Alkiot 0-10
    # Muuta tietotyypit haluamallasi tavalla -> Seuraavassa esimerkki ensimmäisestä alkioista
    muutettu_varaus = []
    # Ensimmäisen alkion = varaus[0] muunnos
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(str(varaus[1]))
    muutettu_varaus.append(str(varaus[2]))
    muutettu_varaus.append(str(varaus[3]))
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(bool(varaus[8]))
    muutettu_varaus.append(str(varaus[9]))
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    
    return [int(varaus[0]),
        str(varaus[1]),
        str(varaus[2]),
        str(varaus[3]),
        datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        datetime.strptime(varaus[5], "%H:%M").time(),
        int(varaus[6]),
        float(varaus[7]),
        varaus[8].strip() == "True" or varaus[8].strip() == "1",
        str(varaus[9]),
        datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    ]
            
     
def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def tulosta_yhteenvedot(varaukset: list):
    
    yhteenveto_vahvistetut(varaukset)
    yhteenveto_pitkat_varaukset(varaukset)
    yhteenveto_varausten_vahvistusstatus(varaukset)
    yhteenveto_vahvistuksista(varaukset)
    yhteenveto_kokonaistulot(varaukset)
    
    #yhteenveto_nimet(varaukset)
    #yhteenveto_varatut_tilat_ja_pvm(varaukset)
    #yhteenveto_nimi_ja_sahkoposti(varaukset)
    #yhteenveto_varatut_tilat_ja_varaajat(varaukset)
    #yhteenveto_varaukset_pvm(varaukset)
    return


def yhteenveto_vahvistetut(varaukset: list):  
    #Tulostetaan vahvistetut varaukset: Tulosta Nimi, Varattu tila, pv.kk.vvvv klo hh.mm
    vahvistetut = [varaus for varaus in varaukset[1:] if varaus[8] == True] 
    #print(f" {varaus[8]}")
    print(f"1) Vahvistetut varaukset: {len([varaus for varaus in varaukset[1:] if varaus[8] == True])}")
    for varaus in varaukset[1:]:
        if varaus[8] == True:
            print(f"- {varaus[1]}       {varaus[9]}        {varaus[4].strftime('%d.%m.%Y')}      klo {varaus[5].strftime('%H.%M')}")
    print()
    return

def yhteenveto_pitkat_varaukset(varaukset: list):  
    #Tuostetaan pitkät varaukset >3h: Tulosta Nimi, pv.kk.vvvv klo hh.mm, kesto X h, Varattu tila
    print(f"2) Pitkät varaukset (≥ 3 h): {len([varaus for varaus in varaukset[1:] if varaus[6] >= 3])}")
    for varaus in varaukset[1:]:
        if varaus[6] >= 3:
            print(f"- {varaus[1]}        {varaus[4].strftime('%d.%m.%Y')}      klo {varaus[5].strftime('%H.%M')} {varaus[6]}h {varaus[9]} ")
    print()
    return

def yhteenveto_varausten_vahvistusstatus(varaukset: list):  
    # Tulostetaan vahvistusstatus
    # Nimi → Vahvistettu
    # Nimi → EI vahvistettu
    print("3) Varausten vahvistusstatus:")
    for varaus in varaukset[1:]:
        status = "Vahvistettu" if varaus[8] == True else "Ei vahvistettu"
        print(f"- {varaus[1]} -> {status}")
    print()
    return

def yhteenveto_vahvistuksista(varaukset: list):  
    # Tulostetaan vahvistettujen ja ei-vahvistettujen varauksien lukumäärät
    # - Vahvistettuja varauksia: X kpl
    # - Ei-vahvistettuja varauksia: Y kpl
    vahvistetut_maara = len([varaus for varaus in varaukset[1:] if varaus[8] == True])
    ei_vahvistetut_maara = len([varaus for varaus in varaukset[1:] if varaus[8] == False])
    print("4) Yhteenveto vahvistuksista:")
    print(f"- Vahvistettuja varauksia: {vahvistetut_maara} kpl")
    print(f"- Ei-vahvistettuja varauksia: {ei_vahvistetut_maara} kpl")
    print()
    return


def yhteenveto_kokonaistulot(varaukset: list):  
    # Tulostetaan vahvistettujen varausten kokonaistulot
    # Vahvistettujen varausten kokonaistulot: 243,50 €
    kokonaistulot = sum(varaus[7] for varaus in varaukset[1:])
    print("5) Vahvistettujen varausten kokonaistulot:")
    print(f"- Kokonaistulot: {str(f'{kokonaistulot:.2f}').replace('.', ',')} €")
    print()
    return

def yhteenveto_nimet(varaukset: list):  
    
    print("Varaajien nimet:")
    for varaus in varaukset[1:]:
        print(f"- {varaus[1]}")
    print()
    return

def yhteenveto_varatut_tilat_ja_pvm(varaukset: list):  
    print("Varatut tilat ja varauspäivät:")
    tilat = set()
    for varaus in varaukset[1:]:    
        tilat.add(varaus[9])    
    for tila in tilat:
        print(f"- {tila} ({varaus[4]})") 
    print()
    return

def yhteenveto_nimi_ja_sahkoposti(varaukset: list):  
    print("Varaajien nimet ja sähköpostit:")
    for varaus in varaukset[1:]:
        print(f"- {varaus[1]} ({varaus[2]})")
    print()
    return

def yhteenveto_varatut_tilat_ja_varaajat(varaukset: list):  
    print("Varatut tilat ja varaajat:")
    for varaus in varaukset[1:]:
        print(f"- {varaus[9]} varannut {varaus[1]}")
    print()
    return
  
def yhteenveto_varaukset_pvm(varaukset: list):  
    print("Varaukset ja varauspäivät:")
    for varaus in varaukset[1:]:
        print(f"- {varaus[1]} varannut päivälle {varaus[4]}")
    print()
    return

def hae_varaukset(varaustiedosto: str) -> list:
    # HUOM! Tälle funktioille ei tarvitse tehdä mitään!
    # Jos muutat, kommentoi miksi muutit
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def main():
    # HUOM! seuraaville riveille ei tarvitse tehdä mitään osassa A!
    # Osa B vaatii muutoksia -> Esim. tulostuksien (print-funktio) muuttamisen.
    # Kutsutaan funkioita hae_varaukset, joka palauttaa kaikki varaukset oikeilla tietotyypeillä
    varaukset = hae_varaukset("varaukset.txt")
    tulosta_yhteenvedot(varaukset)
    #print(" | ".join(varaukset[0]))
    #print("------------------------------------------------------------------------")
    #for varaus in varaukset[1:]:
    #    print(" | ".join(str(x) for x in varaus))
    #    tietotyypit = [type(x).__name__ for x in varaus]
    #    print(" | ".join(tietotyypit))
    #    print("------------------------------------------------------------------------")

if __name__ == "__main__":
    main()