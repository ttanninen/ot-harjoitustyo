# Käyttöohje

Lataa viimeisin [release](https://github.com/ttanninen/ot-harjoitustyo/releases)

## Käyttöliittymä
<img width="614" height="142" alt="GUI2" src="https://github.com/user-attachments/assets/ba77116e-f685-4eac-a63a-5f55fea336c7" />


Sovelluksen kaikki toiminnallisuus tapahtuu sekvensserinäytössä. Ohjelmassa on valmiiksi esimerkkisekvenssi käynnistyessään.

### Sekvenssin toiminnot
- Play: Käynnistää toiston
- Pause: Keskeyttää toiston nykyisen askeleen kohdalle
- Stop: Pysäyttää toiston ja siirtyy sekvenssin alkuun
- BPM: Sekvenssin tempo
- Steps: Sekvenssin askelten lukumäärä
- Steps per beat: Askelten määrä tahdissa
- Add track: Luo uusi raita wav-tiedostosta
- Load sequence: Lataa tallennettu sekvenssi .seqjson tiedostosta
- Save sequence: Tallenna nykyinen sekvenssi .seqjson tiedostoon
- Export wav: Tallenna nykyinen sekvenssi .wav tiedostoon
- Clear pattern: Tyhjentää piirretyt askeleet

### Raidan toiminnot:
- Rename: Nimeä raita uudelleen
- Vol: Raidan äänenvoimakkuus
- Pan: Raidan stereo-panorointi (vasen/oikea)
- Nuoli ylös: Siirrä raita järjestyksessä yksi ylöspäin
- Nuoli alas: Siirra raita järjestyksessä yksi alaspäin
- Punainen ruksi: Poista raita

### Askelraita:
- Vihreä: Toista ääni
- Tummanharmaa/harmaa: Tyhjä askel. Värisävyt visualisoivat tahteja.

## Ohjelman käyttö

Sekvensseriä käytetään hiirellä ja näppäimistöllä. Askelraitojen askeleet aktivoidaan tai deaktivoidaan klikkaamalla hiiren vasemmalla napilla. Vihreä askel tarkoittaa, että raidan äänitiedosto soitetaan kyseisellä askeleella. Tahdin määrittämisen helpottamiseksi, askelraita on väritetty kahdella harmaan sävyllä joka määräytyy valitun tahtilajin mukaan. Askelraidan yläpuolella on askelindikaattori jonka punainen valo merkitsee nykyisen askeleen.

Sekvenssin toisto käynnistetään joko painamalla välilyöntiä tai klikkaamalla ```Play``` painiketta. Sekvenssin toisto pysäytetään joko painamalla välilyöntiä uudestaan tai klikkaamalla ```Stop```. Kaikki ohjelman toiminnot toimivat sekvenssiä toistaessa. Näiden lisäksi ```Pause``` napilla sekvenssin toisto pysäytetään vuorossa olevan askeleen kohdalle. Toisto jatkuu tästä kohdasta painamalla ```Play``` nappia.

Sekvenssin asetuksia voi säätää valitsemalla esimerkiksi tekstikentän ```BPM``` ja kirjoittamalla tähän uuden arvon ja joko painamalla enteriä tai siirtymällä pois tekstikentästä. Mikäli arvo on kelvollinen, se muuttuu ja muussa tapauksessa kenttään palautuu nykyinen arvo.

Sekvenssin pituutta vaihdettaessa lyhyemmäksi kuin nykyinen sekvenssi, pyyhkiytyvät jo piirretyt askeleet pois. Pituutta lisättäessä viimeisen askeleen perään lisätään tyhjiä askeleita valittu määrä. Sekvenssin maksimipituus on 32 askelta. Jo piirretyn sekvenssin voi tyhjentää ```Clear pattern``` painikkeesta.

Sekvenssi voidaan tallentaa joko .seqjson muotoisena json-tiedostona, johon on tallennettu kaikki sekvenssin tiedot tai yksikanavaisena .wav tiedostona. ```Save sequence``` napilla aukeaa tiedostohallintaikkuna johon syötetään tallennettavan ```.seqjson``` tiedoston nimi. Oletuskansio tallennetuille sekvensseille on ohjelman juurihakemistossa kansio ```/projects/```. "Load sequence" napilla aukeaa tiedostohallintaikkuna jolla avataan haluttu ```.seqjson``` tiedosto. Tässäkin oletushakemistona on ```/projects/```. ```Export wav``` napilla aukeaa myös tiedostohallintaikkuna, jossa valitaan tallennettavan wav tiedoston nimi. Sekvenssien wav tallennuksille oletuskansiona on ohjelman juurihakemistossa oleva ```exports```.

Ohjelma suljetaan painamalla ruksia ikkunan oikeasta yläkulmasta.
