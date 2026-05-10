# Testausdokumentti #

Ohjelmaa on testattu perusteellisesti automaattisilla unittesteillä sekä manuaalisesti järjestelmätesteillä.

## Yksikkö- ja integraatiotestaus ##

Jokaiselle sovelluslogiikasta vastaavalle pakkaukselle on laadittu automaattiset yksikkö- ja integraatiotestit. Sovelluslogiikan testeissä hyödynnetään soveltuvissa kohdissa testiäänitiedostoja.  [Audioengine_test](https://github.com/ttanninen/ot-harjoitustyo/blob/main/sequencer-app/src/tests/audioengine_test.py) testaa luokkien ```Audio_file``` ja ```AudioEngine``` toimivuutta, sekä näiden yhteistoimintaa pakkauksen ```sequencer``` olioiden kanssa.
Vastaavasti pakkaus [sequencer_test](https://github.com/ttanninen/ot-harjoitustyo/blob/main/sequencer-app/src/tests/sequencer_test.py) testaa luokkien ```Track``` ja ```Sequence``` omia toimintoja sekä niiden toimivuutta ```AudioEngine``` pakkauksen kanssa. Sovelluksen kontekstihallinnan pakkausta ```app``` testataan pakkauksella [app_test](https://github.com/ttanninen/ot-harjoitustyo/blob/main/sequencer-app/src/tests/app_test.py).

Viimeisimpänä testipakkauksena on [files_test](https://github.com/ttanninen/ot-harjoitustyo/blob/main/sequencer-app/src/tests/files_test.py), joka sisältää yksikkö- ja integraatiotestit tiedostojen käsittelymetodeille. Nämä testit luovat automaattitestauksessa testitiedostot, jotka poistetaan jokaisen testin jälkeen. 

Käyttöliittymä ```ui``` ja sovelluksen pääloopin käynnistävä pakkaus ```index``` on jätetty testikattavuuden ulkopuolelle.

## Testikattavuus ##

Ilman käyttöliittymää ohjelman automaattitestien haaraumakattavuus on 93%.

<img width="617" height="311" alt="image" src="https://github.com/user-attachments/assets/9235e6d3-205a-4e85-aaf4-c8714a2c859f" />

Testaamatta jäivät ohjelmaloopin käynnistävä ```index``` pakkaus, sekä ```Audioengine``` luokan olion generaattorifunktion osa, joka tarkistaa, onko audio streamin jonossa ääniä, joiden soiminen ei ole vielä päättynyt. Tämän toimivuus on kuitenkin varmistettu manuaalisesti ohjelmaa testatessa.


## Järjestelmätestaus ##

Ohjelman toimivuus on testattu asentamalla se [käyttöohjeiden](https://github.com/ttanninen/ot-harjoitustyo/blob/main/sequencer-app/dokumentaatio/kayttoohje.md) mukaisesti windows ja linux ympäristöihin ja manuaalisesti testaamalla [vaatimusmäärittelyssä](https://github.com/ttanninen/ot-harjoitustyo/blob/main/sequencer-app/dokumentaatio/vaatimusmaarittely.md) lueteltujen ominaisuuksien toimivuutta eri syötteillä ja skenaarioilla.


## Laatuongelmat ##

Ohjelman sekvenssin raitojen määrää ei ole rajoitettu, mutta käyttöliittymää tai äänimoottorin toimintaa ei ole testattu tai suunniteltu valtavien raita/audiomäärien käsittelyyn. Ohjelman äänimoottori on perin yksinkertainen ja erityisesti ohjelman juuri käynnistyttyä askelten toistossa on kuultavissa pientä heiluntaa ja nykimistä. Tämä ongelma kuitenkin poistuu yleensä ensimmäisen loopin jälkeen. 

Tarkkakorvaiset sekvensseriohjelmoijat myös varmasti huomaavat, että sekvenssissä on kuultavissa aina pieni keinunta (shuffle), eikä askelten ajoitus ole siis aivan millisekunnin tarkkaa. 
