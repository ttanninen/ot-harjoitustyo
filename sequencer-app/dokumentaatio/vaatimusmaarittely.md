# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi rakentaa lyhyitä looppaavia audiosekvenssejä, esim. rumpukomppeja, käyttämällä lyhyitä äänitiedostoja jotka sovellus toistaa käyttäjän valitsemassa järjestyksessä eri raidoilla. Valmiin sekvenssin voi tallentaa .wav muodossa.

## Käyttöliittymä

Sovelluksessa on graafinen käyttöliittymä, jota käytetään hiirellä. Sekvenssi muodostetaan valitsemalla hiiren osoittimella askeleet, joilla valitun raidan äänitiedosto toistetaan.

## Toiminnallisuus

- Käyttäjä voi valita sekvenssin asetukset
  - Pituus (askelten määrä) TEHTY
  - Nopeus (tempo)TEHTY
  - Raitojen määrä (eli sekvenssissä käytettävä äänitiedostojen määrä) TEHTY
- Käyttäjä voi ladata .wav- muotoisia äänitiedostoja raidoille TEHTY
  - Sovelluksessa on mukana tekijänoikeusvapaita äänitiedostoja ohjelman testaamiseksi TEHTY
- Käyttäjä voi säätää raidan äänenvoimakkuutta TEHTY
- Sekvenssin toiston voi käynnistää ja pysäyttää TEHTY
- Sekvenssin voi tallentaa .wav muotoiseksi äänitiedostoksi TEHTY
- Sekvenssin voi tallentaa tiedostoon TEHTY
- Tallennetun sekvenssin voi ladata tiedostosta TEHTY

## Toteutus

- Käyttöliittymä: TKinter TEHTY OSITTAIN
- Äänitiedostojen toisto: Pygame mixer tai pyaudio TEHTY
- Äänitiedostojen tallennus: pydub
- Sekvenssin askeleiden tallennus: SQLite3

## Jatkokehitysideoita

- Useamman sekvenssin toistaminen järjestyksessä
- Äänikirjaston hallinta
- Äänitiedostojen korvaaminen sovelluksen tuottamilla äänillä
- Muiden äänitiedostomuotojen tukeminen
- Kokonaisten projektien tallentaminen
- Askeleiden manipulointi, esim. pitch
