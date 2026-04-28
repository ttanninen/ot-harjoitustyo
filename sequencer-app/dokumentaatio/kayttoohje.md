# Käyttöohje

Lataa viimeisin [release](https://github.com/ttanninen/ot-harjoitustyo/releases)

## Käyttöliittymä
<img width="614" height="142" alt="GUI_Release_2" src="https://github.com/user-attachments/assets/ab5da76f-25e0-4161-ae6a-28a07c5075db" />

Sovelluksen kaikki toiminnallisuus tapahtuu sekvensserinäytössä. Ohjelmassa on valmiiksi esimerkkisekvenssi käynnistyessään.

### Sekvenssin toiminnot
- Play: Käynnistää toiston
- Pause: Keskeyttää toiston nykyisen askeleen kohdalle
- Stop: Pysäyttää toiston ja siirtyy sekvenssin alkuun
- Clear pattern: Tyhjentää piirretyt askeleet
- BPM: Sekvenssin tempo
- Steps: Sekvenssin askelten lukumäärä
- Steps per beat: Askelten määrä tahdissa
- Add Track: Luo uusi raita wav-tiedostosta

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

Sekvensseriä käytetään hiirellä ja näppäimistöllä. Askelraitojen askeleet aktivoidaan tai deaktivoidaan klikkaamalla hiiren vasemmalla napilla. Vihreä askel tarkoittaa, että raidan äänitiedosto soitetaan kyseisellä askeleella. Askelraita on väritetty kahdella harmaan sävyllä joka määräytyy valitun tahtilajin mukaan. Askelraidan yläpuolella on askelindikaattori jonka punainen valo merkitsee nykyisen askeleen.

Sekvenssin toisto käynnistetään joko painamalla välilyöntiä tai klikkaamalla "Play" painiketta. Sekvenssin toisto pysäytetään joko painamalla välilyöntiä uudestaan tai klikkaamalla "Stop". Kaikki ohjelman toiminnot toimivat sekvenssiä toistaessa.

Sekvenssin asetuksia voi säätää valitsemalla esimerkiksi tekstikentän "BPM" ja kirjoittamalla tähän uuden arvon ja joko painamalla enteriä tai siirtymällä pois tekstikentästä. Mikäli arvo on validi, se muuttuu ja muussa tapauksessa kenttään palautuu nykyinen arvo.

Sekvenssin pituutta vaihdettaessa lyhyemmäksi kuin nykyinen sekvenssi, pyyhkiytyvät jo piirretyt askeleet pois. Pituutta lisättäessä viimeisen askeleen perään lisätään tyhjiä askeleita valittu määrä. Sekvenssin maksimipituus on 32 askelta. Jo piirretyn sekvenssin voi tyhjentää "Clear pattern" painikkeesta.
