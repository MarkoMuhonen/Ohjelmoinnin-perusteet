> [!NOTE]
> Materiaali on luotu ChatGPT:n ja Copilotin avulla.

# 🐍 Yksi toiminnallisuus – neljä eri koodia

## 🎯 Tehtävän tavoite

* Tässä tehtävässä tutustut ohjelmoinnin ja kehitysympäristön perusasioihin.
Opit käyttämään **Visual Studio Codea**, **Pythonia** ja **Git-versionhallintaa**.
* Lisäksi tutustut koodin kehitykseen askel askeleelta: 👉 yksinkertaisesta versiosta kohti virallista ja ammattimaisempaa ohjelmaa. 
* Valmiin Python-koodin avulla luet tiedoston, jossa on **yksi sana**, ja ohjelma tulostaa sen **konsoliin**.
* Lopuksi jaat koodin omaan GitHub-repoosi ja kuittaat tehtävän tehdyksi **Itslearningiin**.

> [!NOTE]
> Halutessa työn voi tehdä pareittain. Tällöin kohdassa [Palautusohje Itslearningiin](#-palautusohje-itslearningiin) pari tekee vain yhden palautuksen, johon on yhdistetty molemmat.

---

## 🧰 Tarvittavat työkalut

* **Visual Studio Code**
* **Python 3.10 tai uudempi**
* **Git** ja **GitHub-tili**

---

## 📁 Projektin rakenne

```

📁 Viikko1/
├─ 📁 versio1_yksinkertainen/
│  ├─ 🐍 tulosta_sana_v1.py
│  └─ 📄 sana.txt
│
├─ 📁 versio2_main/
│  ├─ 🐍 tulosta_sana_v2.py
│  └─ 📄 sana.txt
│
├─ 📁 versio3_virhekasittely/
│  ├─ 🐍 tulosta_sana_v3.py
│  └─ 📄 sana.txt
│
└─ 📁 versio4_virallinen/
   ├─ 🐍 tulosta_sana_v4.py
   └─ 📄 sana.txt


```

💡 Jokaisessa kansiossa on oma Python-skripti ja oma `sana.txt`.

---

## 🧭 Työvaiheet vaihe vaiheelta

### 🧱 1️⃣ Luo uusi GitHub-repositorio

1. Mene osoitteeseen 👉 [https://github.com](https://github.com)
2. Kirjaudu sisään omalla GitHub-tunnuksellasi.
3. Paina oikeasta yläkulmasta **“+” → “New repository”**.
4. Täytä tiedot:

   * **Repository name:** esim. `OhjelmoinninPerusteet`
   * **Description:** (valinnainen)
   * Valitse **Public**
   * Voit **jättää README:n tyhjäksi** (lisätään myöhemmin)
5. Paina **“Create repository”** 🎉

---

### 💻 2️⃣ Avaa Visual Studio Code

1. Avaa **Visual Studio Code**.
2. Valitse **View → Command Palette...** tai paina `Ctrl + Shift + P`.
3. Kirjoita hakukenttään:

   ```
   Git: Clone
   ```
4. Valitse **Git: Clone**.
5. Liitä GitHubin antama kloonausosoite (esim.):

   ```
   https://github.com/oma-kayttaja/OhjelmoinninPerusteet.git
   ```
6. Valitse kansio omalta koneeltasi, johon haluat tallentaa projektin.
7. Kun kloonaus on valmis, Visual Studio Code kysyy:
   👉 “Would you like to open the cloned repository?”
   → Valitse **Open**.

---

### 🧩 3️⃣ Tarkista yhteys

Avaa VS Coden **Terminal** (pikanäppäin `Ctrl + ö` tai `Ctrl + Shift + ñ`) ja kokeile:

```bash
git status
```

Jos saat viestin kuten:

```
On branch main
nothing to commit, working tree clean
```

✅ Repo on kunnolla kloonattu ja yhteys toimii!

---

### 📤 4️⃣ Lisää tai kopioi kansiot ja tiedostot projektiin

* Lisää kansiot ja tiedostot, esim. ladatut koodiversiot (`v1_…`, `v2_…`, jne.)
> Katso [Projektin kansiorakenne](#-projektin-rakenne)
* Tee commit ja lähetä muutokset GitHubiin (Onnistuu myös Visual Studio Codesta graafisesti):

```bash
git add .
git commit -m "Lisätty Viikko1"
git push
```

---

## 🌐 5️⃣ Tarkista GitHubissa

Palaa selaimeen ja päivitä GitHub-sivu.
Näet nyt kaikki lisäämäsi tiedostot! 🎉

---

## 🐍 6️⃣ Testaa ohjelmien toiminta

Avaa VS Coden terminaali ja suorita komennot peräkkäin:

```bash
cd versio1_yksinkertainen
python tulosta_sana_v1.py
````

```bash
cd ..\versio2_main
python tulosta_sana_v2.py
```

```bash
cd ..\versio3_virhekasittely
python tulosta_sana_v3.py
```

```bash
cd ..\versio4_virallinen
python tulosta_sana_v4.py
# tai:
python tulosta_sana_v4.py --tiedosto sana.txt
```
> [!TIP]
> Kokeile myös `python tulosta_sana_v4.py --help` nähdäksesi ohjelman oman ohjeen!

---

## 7️⃣ ✨ Ohjelmiin tutustuminen

1. Tutustu ohjelmatiedostojen sisältöön
2. Yritä selvittää, että miksi ohjelmat toimivat kuten toimivat
3. Kokeile muuttaa myös tiedoston `sanat.txt` sisältöä. Varmista, että muutos näkyy ohjelman suorituksen jälkeen.

---

## 📤 Palautusohje Itslearningiin

Palauta **linkki GitHub-repoon** ja **kuvankaappaus konsolista**, jossa näkyy ohjelman suoritus ja tulostettu sana.

Lisää palautukseen myös lyhyt teksti:
> Mitä jäi päällimmäisenä tehtävästä mieleen?

---

## 💬 Hyvä fiilis tekemiseen!

**Muista:** kaikki ohjelmoijat aloittavat jostain.
Tärkeintä ei ole täydellinen koodi, vaan **oppiminen, kokeilu ja oivallus**.
Pidä hauskaa ja tutki, miten pieni skripti voi kehittyä vaihe vaiheelta suuremmaksi kokonaisuudeksi! 🚀💡😎

---

## 💡 Yleisimmät virheet ja ratkaisut

| Virhe | Syy | Ratkaisu |
|-------|-----|----------|
| “Tiedostoa ei löydy” | Skriptiä ajetaan väärässä kansiossa | Siirry kansioon jossa skripti on |
| “Tiedoston sisältö virheellinen” | Tiedostossa useampi sana | Jätä vain yksi sana, ei välilyöntejä |
| “Komento ei toimi PowerShellissä” | Suorituspolitiikka estää aktivoinnin | Aja `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |