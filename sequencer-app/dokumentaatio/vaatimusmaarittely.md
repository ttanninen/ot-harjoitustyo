# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksella voi rakentaa lyhyitä looppaavia audiosekvenssejä, esim. rumpukomppeja, käyttämällä lyhyitä äänitiedostoja jotka sovellus toistaa käyttäjän valitsemassa järjestyksessä eri raidoilla. Valmiin sekvenssin voi tallentaa .wav muodossa.

## Käyttöliittymä

Sekvenssi rakentuu raidoista, joista jokainen pitää sisällään yhden äänitiedoston. Sekvenssin pituus määrittelee raitojen pituuden. Sovelluksessa on graafinen käyttöliittymä, jota käytetään hiirellä ja näppäimistöllä. Sekvenssi muodostetaan valitsemalla hiiren osoittimella askeleet, joilla valitun raidan äänitiedosto toistetaan. Sekvenssin nopeutta, pituutta sekä tahtilajia voi muuttaa muokkaamalla käyttöliittymän tekstikentissä olevia arvoja.

## Toiminnallisuus

- Käyttäjä voi valita sekvenssin asetukset:
  - Pituus
  - Nopeus
  - Tahtilaji
  - Raitojen määrä
- Käyttäjä voi valita raitojen asetukset:
  - Raidalla toistettava .wav-muotoinen äänitiedosto
    - Sovelluksessa on mukana tekijänoikeusvapaita äänitiedostoja ohjelman testaamiseksi
  - Käyttäjä voi nimetä raidan uudelleen
  - Käyttäjä voi säätää raidan äänenvoimakkuutta
  - Käyttäjä voi säätää raidan stereopanorointia (vasen / oikea)
  - Käyttäjä voi lisätä ja poistaa raidan
  - Käyttäjä voi valita raidan askeleet, joilla äänitiedosto toistetaan.

- Sekvenssin toiston voi käynnistää ja pysäyttää
- Sekvenssin voi tallentaa .wav muotoiseksi äänitiedostoksi
- Sekvenssin voi tallentaa json-muotoiseen tiedostoon
- Tallennetun sekvenssin voi ladata json-tiedostosta

## Toteutus

- Käyttöliittymä: TKinter
- Äänitiedostojen toisto: Miniaudio
- Äänitiedostojen tallennus: Scipy.io
- Sekvenssin tallennus: Json

## Jatkokehitysideoita

- Useamman sekvenssin toistaminen järjestyksessä
- Äänikirjaston hallinta
- Äänitiedostojen korvaaminen sovelluksen tuottamilla äänillä
- Muiden äänitiedostomuotojen tukeminen
- Kokonaisten projektien tallentaminen
- Askeleiden manipulointi, esim. pitch
