## Viikko 3
- Luotu luokat raidoille ja sekvensserille perusominaisuuksilla
- Perusominaisuuksien rakennusta varten käytössä lähinnä pygame, joka ei sovellu tarkkaan äänentoistoon kovin hyvin. Tämä korjataan tulevaisuudessa.
- Index.py:ssä sovelluslogiikan testausta ja tekstikäyttöinen "käyttöliittymä" jolla voi soittaa valmiiksi tehtyä 16-askeleen looppia yhdellä raidalla.

## Viikko 4
- Suurin muutos äänimoottorin vaihto miniaudioon, joka mahdollistaa monipuolisempia ominaisuuksia yksittäisille raidoille.
- Graafisesta käyttöliittymästä on luotu pohja, jota laajennetaan seuraavalla viikolla.

## Viikko 5
- Sovellus laajentui uusilla ominaisuuksilla kuten raitojen lisäämisellä ja poistamisella ja raitojen äänenvoimakkuuden ja panningin säätö.
- Graafiseen käyttöliittymään lisättiin tahtilajin mukaan määräytyvä värisävytys helpottamaan askelten piirtämistä sekä askeleen ilmaisin.
- Sovelluslogiikkaa muutettiin siten että index.py kutsuu app.py:tä joka luo tarvittavat oliot sekvensserille ja äänimoottorille, ja jota UI kutsuu.

