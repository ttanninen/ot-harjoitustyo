# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi rakentaa lyhyitä looppaavia audiosekvenssejä, esim. rumpukomppeja, käyttämällä lyhyitä äänitiedostoja jotka sovellus toistaa käyttäjän valitsemassa järjestyksessä eri raidoilla. Valmiin sekvenssin voi tallentaa .wav muodossa.

## Käyttöliittymä

Sovelluksessa on graafinen käyttöliittymä, jota käytetään hiirellä. Sekvenssi muodostetaan valitsemalla hiiren osoittimella askeleet, joilla valitun raidan äänitiedosto toistetaan.

## Toiminnallisuus

- Käyttäjä voi valita sekvenssin asetukset
  - Pituus (askelten määrä)
  - Nopeus (tempo)
  - Raitojen määrä (eli sekvenssissä käytettävä äänitiedostojen määrä)
- Käyttäjä voi ladata .wav- muotoisia äänitiedostoja raidoille
  - Sovelluksessa on mukana tekijänoikeusvapaita äänitiedostoja ohjelman testaamiseksi
- Käyttäjä voi säätää raidan äänenvoimakkuutta
- Sekvenssin toiston voi käynnistää ja pysäyttää TEHTY
- Sekvenssin voi tallentaa .wav muotoiseksi äänitiedostoksi
- Sekvenssin askeleet voi tallentaa tietokantaan muistiin
- Tallennetun sekvenssin askeleet voi ladata tietokannasta

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
