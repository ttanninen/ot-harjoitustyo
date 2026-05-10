# Testausdokumentti #

Ohjelmaa on testattu perusteellisesti automaattisilla unittesteillä sekä manuaalisesti järjestelmätesteillä.

## Yksikkö- ja integraatiotestaus ##

Jokaiselle sovelluslogiikasta vastaavalle pakkaukselle on laadittu automaattiset yksikkö- ja integraatiotestit. Sovelluslogiikan testeissä hyödynnetään soveltuvissa kohdissa testiäänitiedostoja.  ```Audioengine_test``` testaa luokkien ```Audio_file``` ja ```AudioEngine``` toimivuutta, sekä näiden yhteistoimintaa pakkauksen ```sequencer``` olioiden kanssa.
Vastaavasti pakkaus ```sequencer_test``` testaa luokkien ```Track``` ja ```Sequence``` omia toimintoja sekä niiden toimivuutta ```AudioEngine``` pakkauksen kanssa. Sovelluksen kontekstihallinnan pakkausta ```app``` testataan pakkauksella ```app_test```.

Viimeisimpänä testipakkauksena on ```files_test```, joka sisältää yksikkö- ja integraatiotestit tiedostojen käsittelymetodeille. Nämä testit luovat automaattitestauksessa testitiedostot, jotka poistetaan jokaisen testin jälkeen. 

Käyttöliittymä ```ui``` ja sovelluksen pääloopin käynnistävä pakkaus ```index``` on jätetty testikattavuuden ulkopuolelle.

## Testikattavuus ##

Ilman käyttöliittymää ohjelman automaattitestien haaraumakattavuus on 93%.

<img width="617" height="311" alt="image" src="https://github.com/user-attachments/assets/9235e6d3-205a-4e85-aaf4-c8714a2c859f" />

Testaamatta jäivät ohjelmaloopin käynnistävä ```index``` pakkaus, sekä ```Audioengine``` luokan olion generaattorifunktion osa, joka tarkistaa, onko audio streamin jonossa ääniä, joiden soiminen ei ole vielä päättynyt. Tämän toimivuus on kuitenkin varmistettu manuaalisesti ohjelmaa testatessa.


## Järjestelmätestaus ##

Ohjelman toimivuus on testattu asentamalla se käyttöohjeiden mukaisesti windows ja linux ympäristöihin ja manuaalisesti testaamalla ominaisuuksien toimivuutta eri syötteillä ja skenaarioilla.


## Laatuongelmat ##

Ohjelman sekvenssin raitojen määrää ei ole rajoitettu, mutta käyttöliittymää tai äänimoottorin toimintaa ei ole testattu tai suunniteltu valtavien raita/audiomäärien käsittelyyn. ohjelman äänimoottori on yksinkertainen ja erityisesti ohjelman juuri käynnistyttyä askelten toistossa on kuultavissa pientä heiluntaa ja nykimistä. Tämä kuitenkin poistuu yleensä ensimmäisen loopin jälkeen. 
