# Copyright (c) 2025 Marko Muhonen
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.
#
#
# Tässä käytetään olioita ja luokkia varauksien käsittelyyn.
# Ohjelma lukee varaukset tiedostosta ja käsittelee niitä olioina.
#
# Tämä oli minulle uutta, tein aikaisemmin sanakirja-pohjaisen ratkaisun, 
# nyt piti sitten kokeilla olioita ja luokkia tässä koodissa
#
# Listaan verrattuna olioilla on etuna se, että data ja siihen liittyvät toiminnot
# voidaan kapseloida yhteen paikkaan, mikä parantaa koodin luettavuutta ja selkeyttä.
#  
########################################################################################

from datetime import datetime

class Varaus:
    """
    Luokka yksittäisen varauksen tietojen tallentamiseen ja käsittelyyn.
    """

    @classmethod
    def from_string(cls, rivi: str) -> "Varaus":
        """
        Luo Varaus-olion tiedostorivistä.
        :param rivi: Yksi varausrivi merkkijonona (kentät eroteltu |)
        :return: Varaus-olio
        """
        varaustiedot = rivi.strip().split('|')
        return muunna_varaustiedot(varaustiedot)
    
    def __init__(self, varaus_id, nimi, sahkoposti, puhelin,
                 paiva, kellonaika, kesto, hinta,
                 vahvistettu, kohde, luotu):
        """
        Alustaa Varaus-olion kentät.
        """
        self.varaus_id = varaus_id
        self.nimi = nimi
        self.sahkoposti = sahkoposti
        self.puhelin = puhelin
        self.paiva = paiva
        self.kellonaika = kellonaika
        self.kesto = kesto
        self.hinta = hinta
        self.vahvistettu = vahvistettu
        self.kohde = kohde
        self.luotu = luotu

    def is_confirmed(self):
        """
        Palauttaa True jos varaus on vahvistettu, muuten False.
        """
        return self.vahvistettu

    def is_long(self):
        """
        Palauttaa True jos varauksen kesto on vähintään 3 tuntia.
        """
        return self.kesto >= 3

    def total_price(self):
        """
        Palauttaa varauksen kokonaishinnan (kesto * hinta).
        """
        return self.kesto * self.hinta

def muunna_varaustiedot(varaus: list[str]) -> Varaus:
    """
    Muuntaa varauslistan Varaus-olioksi.
    :param varaus: Lista varauksen kentistä merkkijonoina
    :return: Varaus-olio
    """
    return Varaus(
        varaus_id=int(varaus[0]),
        nimi=varaus[1],
        sahkoposti=varaus[2],
        puhelin=varaus[3],
        paiva=datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        kellonaika=datetime.strptime(varaus[5], "%H:%M").time(),
        kesto=int(varaus[6]),
        hinta=float(varaus[7]),
        vahvistettu=varaus[8].lower() == "true",
        kohde=varaus[9],
        luotu=datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    )

def hae_varaukset(varaustiedosto: str) -> list[Varaus]:
    """
    Lukee varaukset tiedostosta ja palauttaa listan Varaus-olioita.
    :param varaustiedosto: Tiedostonimi, josta varaukset luetaan
    :return: Lista Varaus-olioita
    """
    varaukset = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for rivi in f:
            varaukset.append(Varaus.from_string(rivi))
    return varaukset

def vahvistetut_varaukset(varaukset: list[Varaus]):
    """
    Tulostaa kaikki vahvistetut varaukset.
    :param varaukset: Lista Varaus-olioita
    """
    for varaus in varaukset:
        if varaus.is_confirmed():
            print(f"- {varaus.nimi}, {varaus.kohde}, {varaus.paiva.strftime('%d.%m.%Y')}, {varaus.kellonaika.strftime('%H.%M')}, kesto {varaus.kesto} h")
    print()

def pitkat_varaukset(varaukset: list[Varaus]):
    """
    Tulostaa kaikki pitkät varaukset (kesto vähintään 3 tuntia).
    :param varaukset: Lista Varaus-olioita
    """
    for varaus in varaukset:
        if varaus.is_long():
            print(f"- {varaus.nimi}, {varaus.paiva.strftime('%d.%m.%Y')} klo {varaus.kellonaika.strftime('%H.%M')}, kesto {varaus.kesto} h, {varaus.kohde}")
    print()

def varausten_vahvistusstatus(varaukset: list[Varaus]):
    """
    Tulostaa jokaisen varauksen vahvistusstatuksen.
    :param varaukset: Lista Varaus-olioita
    """
    for varaus in varaukset: 
        if varaus.is_confirmed():
            status = "Vahvistettu"
        else:
            status = "EI vahvistettu"
        print(f"{varaus.nimi} → {status}")
    print()

def varausten_lkm(varaukset: list[Varaus]):
    """
    Tulostaa vahvistettujen ja ei-vahvistettujen varausten lukumäärät.
    :param varaukset: Lista Varaus-olioita
    """
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset:
        if varaus.is_confirmed():
            vahvistetutVaraukset += 1 
        else: 
            eiVahvistetutVaraukset += 1
    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list[Varaus]):
    """
    Tulostaa vahvistettujen varausten kokonaistulot.
    :param varaukset: Lista Varaus-olioita
    """
    varaustenTulot = 0
    for varaus in varaukset:
        if varaus.is_confirmed():
            varaustenTulot += varaus.total_price()

    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()
    
def main():
    """
    Pääohjelma: lukee varaukset tiedostosta ja tulostaa raportit.
    """
    varaukset = hae_varaukset("varaukset.txt")
    
    print()
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)
     

if __name__ == "__main__":
    main()