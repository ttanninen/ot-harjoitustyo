# Ohjelmistotekniikka harjoitustyö

**Yksinkertainen sampleri / sekvensseri**

Sekvensseri toistaa äänitiedostoja järjestyksessä ja samanaikaisesti. Ohjelmalla voi ohjelmoida esimerkiksi lyhyitä rumpukomppeja.
Käyttöliittymä toteutetaan TKinterillä ja äänien toistoon käytetään miniaudio-kirjastoa.

Ominaisuuksia:

- Samplejen lataaminen
- Raidan äänentason säätäminen
- Hiirellä käytettävä käyttöliittymä
- Gridin pituuden määritteleminen (Esim. 0-16 askelta) (Todo)
- Sekvenssin tallentaminen .wav:iksi (Todo)
- Sekvenssin looppaaminen

## Asennus ja käynnistys

Asenna aluksi ohjelman vaatimat riippuvuudet:
```bash
poetry install
```

Sovellus käynnistetään komennolla:
```bash
poetry run invoke start
```

## Sovelluksen testauksen komentorivikomennot
Yksikkötestaus:
```bash
poetry run invoke test
```

Testikattavuusraportin luominen ```sequencer-app/htmlcov/``` -kansioon:
```bash
poetry run invoke coverage-report
```

Pylint tarkastus:
```bash
poetry run invoke lint
```

## Release

## Dokumentaatio


- [Vaatimusmäärittely](/sequencer-app/dokumentaatio/vaatimusmaarittely.md)
- [Tuntikirjanpito](/sequencer-app/dokumentaatio/tuntikirjanpito.md)
- [Changelog](/sequencer-app/dokumentaatio/changelog.md)
- [Arkkitehtuuri](/sequencer-app/dokumentaatio/arkkitehtuuri.md)
