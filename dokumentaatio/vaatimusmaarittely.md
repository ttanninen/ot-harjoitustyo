# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi sekvensoida looppaavia äänitallenteita, esim. rumpukomppeja, käyttämällä lyhyitä äänitiedostoja jotka ohjelma toistaa käyttäjän valitsemassa järjestyksessä eri raidoilla.

## Käyttöliittymä

Sovelluksessa on graafinen käyttöliittymä, jota käytetään hiirellä. Sekvenssi muodostetaan valitsemalla askeleet, joilla valitun raidan äänitiedosto toistetaan kussakin kohtaa.

## Toiminnallisuus

- Käyttäjä voi valita sekvenssin asetukset
  - Pituus
  - Nopeus
  - Tempo
  - Raitojen määrä
- Käyttäjä voi ladata .wav- muotoisia äänitiedostoja raidoille
- Käyttäjä voi säätää raidan äänenvoimakkuutta
- Sekvenssin voi käynnistää ja pysäyttää
- Sekvenssin voi tallentaa .wav muotoiseksi äänitiedostoksi
- Sekvenssin askeleet voi tallentaa tietokantaan muistiin
- Tallennetun sekvenssin askeleet voi ladata tietokannasta

## Toteutus

- Käyttöliittymä: TKinter
- Äänitiedostojen toisto: Pygame mixer tai pyaudio
- Äänitiedostojen tallennus: pydub
- Sekvenssin askeleiden tallennus: SQLite3

## Jatkokehitysideoita

- Useamman sekvenssin toistaminen järjestyksessä
- Äänitiedostojen korvaaminen sovelluksen tuottamilla äänillä
- Muiden äänitiedostomuotojen tukeminen
- Kokonaisten projektien tallentaminen
- Askeleiden manipulointi, esim. pitch
