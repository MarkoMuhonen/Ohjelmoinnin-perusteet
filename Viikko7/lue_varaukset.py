# Copyright (c) 2025 Marko Muhonen
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.

from datetime import datetime

class Varaus:
    def __init__(self, varaus_id, nimi, sahkoposti, puhelin,
                 paiva, kellonaika, kesto, hinta,
                 vahvistettu, kohde, luotu):
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

    # Esimerkkimetodeja
    def is_confirmed(self):
        return self.vahvistettu

    def is_long(self):
        return self.kesto >= 3

    def total_price(self):
        return self.kesto * self.hinta

def muunna_varaustiedot(varaus: list) -> Varaus:
    """
    Muuntaa varauslistan Varaus-olioksi.
    """
    return Varaus(
        int(varaus[0]),
        varaus[1],
        varaus[2],
        varaus[3],
        datetime.strptime(varaus[4], "%Y-%m-%d").date(),
        datetime.strptime(varaus[5], "%H:%M").time(),
        int(varaus[6]),
        float(varaus[7]),
        varaus[8].lower() == "true",
        varaus[9],
        datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S")
    )
def hae_varaukset(varaustiedosto: str) -> list:
    varaukset = []
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset
"""
def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if(varaus[8]):
            print(f"- {varaus[1]}, {varaus[9]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}")

    print()

def pitkat_varaukset(varaukset: list):
    for varaus in varaukset[1:]:
        if(varaus[6] >= 3):
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} h, {varaus[9]}")

    print()

def varausten_vahvistusstatus(varaukset: list):
    for varaus in varaukset[1:]:
        if(varaus[8]):
            print(f"{varaus[1]} → Vahvistettu")
        else:
            print(f"{varaus[1]} → EI vahvistettu")

    print()

def varausten_lkm(varaukset: list):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0
    for varaus in varaukset[1:]:
        if(varaus[8]):
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list):
    varaustenTulot = 0
    for varaus in varaukset[1:]:
        if(varaus[8]):
            varaustenTulot += varaus[6]*varaus[7]

    print("Vahvistettujen varausten kokonaistulot:", f"{varaustenTulot:.2f}".replace('.', ','), "€")
    print()
    """
    
def main():
    varaukset = hae_varaukset("varaukset.txt")
    
    
    
    print("1) Vahvistetut varaukset")
    for varaus in varaukset:
        if varaus.is_confirmed():
            print(f"- {varaus.nimi}, {varaus.kohde}, {varaus.paiva.strftime('%d.%m.%Y')}")
    
    print("2) Pitkät varaukset (≥ 3 h)")
    for varaus in varaukset:
        if varaus.is_long():
            print(f"- {varaus.nimi}, {varaus.paiva.strftime('%d.%m.%Y')} klo {varaus.kellonaika.strftime('%H.%M')}, kesto {varaus.kesto} h, {varaus.kohde}")
    
    #print("3) Varausten vahvistusstatus")
    #varausten_vahvistusstatus(varaukset)
    #print("4) Yhteenveto vahvistuksista")
    #varausten_lkm(varaukset)
    #print("5) Vahvistettujen varausten kokonaistulot")
    #varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()