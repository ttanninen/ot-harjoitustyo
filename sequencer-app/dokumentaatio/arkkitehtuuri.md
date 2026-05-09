# Arkkitehtuurikuvaus

## Ohjelman rakenne
Ohjelman rakenne on kuvattu seuraavassa pakkauskaaviossa:


<img width="692" height="461" alt="sequencer_app_packages" src="https://github.com/user-attachments/assets/fa720d93-e181-4989-98f3-66a0deb3c200" />

\
Ohjelma koostuu neljästä pääkomponentista: Sekvensseristä, äänimoottorista, käyttöliittymästä ja tiedostohallinnasta. Ohessa lyhyt kuvaus kaikista komponenteista ja tiedostojen oletushakemistoista.

__App__ on sovelluksen kontekstinhallitsija. Sen tehtävä on alustaa ja omistaa ```AudioEngine``` sekä ```Sequence``` oliot ja käynnistää tai tarvittaessa sulkea äänivirta (audio stream).

__Sequencer__ sisältää ohjelman päätietomallit eli ```Sequencen``` ja ```Trackin``` eli sekvensserin toiminnallisuudesta huolehtivat luokat. ```Sequence``` sisältää sekvenssin ominaisuudet, kuten tempon ja tahtilajitiedot. ```Sequence``` sisältää listan ```Track``` olioista, jotka sisältävät audiodatan numpy taulukkona sekä toistettavan askelkuvion. 

__AudioEngine__ vastaa äänen toistamisesta miniaudio-kirjaston avulla. Se ylläpitää jonoa soitettavista äänistä ja miksaa ne yhteen reaaliaikaisen generaattorifunktion avulla.

__UI__ eli TKinter-pohjainen käyttöliittymä on eriytetty sekvensserin toimintalogiikasta. Käyttöliittymä piirtää sekvenssin askelruudukon ja työkalupalkit. Käyttöliittymä on pyritty luomaan niin, että mitään sovelluksen toiminnallisuutta ei ole toteutettu ainoastaan käyttöliittymän pakkauksessa.

__Files__ eli tiedostonhallinta vastaa sekvenssin tallentamisesta ja lataamisesta. Sekvenssi tallennetaan tai ladataan JSON-muodossa, jossa äänidata on enkoodattu base64-merkkijonoksi. Tämän lisäksi sekvenssi on mahdollista tallentaa miksattuna yksikanavaisena wav-tiedostona.

__Samples__ hakemisto on oletushakemisto sekvensserin raidoille ladattaville äänitiedostoille. Ohjelma voi kuitenkin avata äänitiedostoja mistä tahansa kansiosta käyttäjän tietokoneella.

__Projects__ hakemisto on oletushakemisto tallennetuille sekvensseille .seqjson -muodossa.

__Exports__ hakemisto on oletushakemisto tallennetuille wav-muotoisille sekvensseille.

## Käyttöliittymä

Käyttöliittymä on rakennettu TKinter-kirjastolla ja se koostuu yhdestä päänäkymästä, joka jakautuu kolmeen pääosaan:
__Työkalupalkki__ sisältää toistokontrollinapit (play/pause/stop), valinnat sekvenssin asetuksista (tempo, pituus, tahtilaji) sekä sekvenssin hallintaan liittyvät työkalut (tallenna/lataa sekvenssi ja lisää uusi raita)

__Askelindikaattori__ näyttää pienet ympyrät työkalupalkin alla, jossa punainen ympyrä näyttää sekvenssin toistopään sijainnin.

__Askelruudukko__ on TKinter-kirjaston grid-elementti, joka jokainen rivi vastaa yhtä raitaa. Jokaisen raidan vasemmassa reunassa on raidan hallintatyökalut (nimi, äänenvoimakkuus, panorointi, järjestyksen muutos ja poisto). Tämän jälkeen tulevat askelnapit, joista jokainen nappi symboloi yhtä askelta. Askelnapin väri kertoo onko askel aktiivinen, eli soitetaanko sillä askeleella ääni vai ei. Askelruudukon taustaväri määräytyy tahtilajin mukaan.

Sekvensseri-ikkunan koko mukautuu dynaamisesti sekvenssin pituuden ja raitojen määrän eli askelruudukon koon mukaan. Raitojen määrää ei ole rajoitettu, mutta sekvenssin maksimipituus on 32 askelta.

## Sovelluslogiikka
Sovellus rakentuu ```app``` moduulin omistamiin ```Sequencer``` ja ```AudioEngine``` luokkiin, jotka alustetaan ```index``` -moduulissa ohjelman käynnistyessä. 

Pakkaus ```audioengine``` on jaettu luokkiin ```AudioFile``` ja ```AudioEngine```. Näiden luokkien metodit luovat toiminnallisuuden wav-tiedostojen käsittelyyn, sekä monen äänen samanaikaiseen toistamiseen. Äänitiedostojen käsittely ja toisto on toteutettu miniaudio-kirjastolla. Miniaudiolla luodaan jatkuva audio stream, joka lähettää ääntä käyttäjän ensisijaiseen äänilaitteeseen. Äänivirtaan lisätyt äänet toistetaan pienellä (oletus: 15 ms) viiveellä, jotta prosessointi ei vaikuta äänen toistoaikaan.

Pakkaus ```Sequencer``` sisältää luokat ```Track``` ja ```Sequence```. Käyttäjän luoma sekvenssi rakennetaan muokkaamalla luokan ```Track```-olioita ja lisäämällä niitä luokan ```Sequence```-olioon omistamaan listaan. Luokka ```Track``` sisältää raidalle ladatun äänidatan sekä askelkuvion, jota sekvenssi toistaa. Askelkuvio syötetään listamuodossa, joka muutetaan numpy taulukoksi, jossa "0" tarkoittaa tyhjää askelta ja "1" soitettavaa askelta. ```Track```sisältää metodit askelkuvion muokkaamiseen.

```Sequencer``` luokka vastaa varsinaisen sekvensserin toiminnasta looppaamalla ```Track```-olioden sisältämiä askelkuvioita läpi ja lähettämällä niiden sisältämiä äänidatatietoja ```audioengine```:lle toistoa varten. ```Sequencer``` sisältää myös kaikki käyttöliittymälle tarjottavat metodit sekvenssin toistamiseen ja raitojen askelien muokkaamiseen. Sekvenssin asetukset, kuten tempo ja tahtilaji ovat myös muokattavissa käyttöliittymän kautta.

Viimeisenä pakkauksena on ```Files```, joka sisältää tiedostojen käsittelyn hoitavat funktiot, eli sekvenssin tallennuksen ja lataamisen sekä wav tiedostojen luonnin. Tiedostohallinnan funktioita kutsutaan käyttöliittymästä.

## Päätoiminnallisuudet

Ohessa muutamia sovelluksen toimintaa esitteleviä esimerkkejä toimintalogiikasta:

### Uuden raidan lisääminen:
\
<img width="519" height="361" alt="add_track_diag drawio" src="https://github.com/user-attachments/assets/981bc41f-4441-4f15-8e1a-ddfd4f5aedda" />
Käyttäjän painaessa "Add Track" nappia käyttöliittymässä aukeaa TKinterin file dialog window. Valittava tiedostomuoto on wav tiedosto. UI palauttaa tiedoston nimen Sequencer-oliolle joka kutsuu load_sound() metodia AudioEngine pakkauksesta (muutetaan myöhemmin omaan tiedostojen käsittelypakkaukseen). Metodi load_sound() tarkistaa että tiedosto on oikeanlainen ja nostaa ValueError virheilmoituksen, mikäli näin ei ole. Mikäli tiedosto on soveltuva, siitä muodostetaan Track-olio, joka lisätään sekvenssiin uudeksi raidaksi. Lopuksi UI kutsuu rebuild_grid() metodia, jolla sekvensserin näkymä päivitetään uuden raidan kanssa.


### Sekvenssin käynnistäminen ja äänen toisto:
\
<img width="779" height="264" alt="play_sound_diagram" src="https://github.com/user-attachments/assets/36433a85-66a3-41c1-ad68-6a8994b35557" />
Käyttäjän painaessa ```Play``` nappia käyttöliittymässä, ```UI._play()``` kutsuu sekvenssin ```Sequence.play()``` funktiota joka käynnistää sekvenssin ```_play_loop()``` metodin omassa säikeessään. ```_play_loop()``` käy sekvenssin askeleita läpi yksi kerrallaan. Jokaisen askeleen kohdalla se tarkistaa mitkä raidat ovat aktiivisia kyseisellä askeleella ja lähettää aktiivisten raitojen äänidatan ```AudioEnginelle```. Metodi ```AudioEngine.play()``` laittaa äänidatan jonoon, josta generaattori poimii sen ja miksaa äänivirran bufferiin. ```_play_loop()``` odottaa joka askeleen jälkeen sekvenssin tempon ja tahtilajin mukaisen ajan ennen siirtymistä seuraavaan askeleeseen. ```UI._poll_step()``` lukee tasaisin väliajoin (16ms) sekvenssin ```current_step```arvon ja päivittää askelindikaattorin valon näytölle.

### Sekvenssin tallentaminen: ###
\
<img width="710" height="362" alt="save_sequence_diag (1)" src="https://github.com/user-attachments/assets/24cb6ea7-591b-44d6-a0db-9cf05efee28e" />
Käyttäjän painaessa ```Save sequence``` nappia, ```UI._save_sequence()``` avaa TKinterin file dialog windowin. Käyttäjän valittua tallennushakemiston ja tiedoston nimen, kutsutaan ```save_sequence(sequence,filename)``` funktiota ```files``` moduulista. Tämä käy läpi kaikki sekvenssin raidat ja tekee jokaiselle raidalle seuraavat toimenpiteet:
- Kirjoittaa äänidatan BytesIO-bufferiin käyttäen ```scipy.io.wavfile.write()``` -funktiota.
- Enkoodaa bufferin sisällön base64-merkkijonoksi.
- Kerää raidan nimen, äänenvoimakkuuden, panoroinnin, askelkuvion ja enkoodatun äänidatan listaan.
Tämän jälkeen ```save_sequence()``` konstruoi JSON-objektin joka sisältää sekvenssin asetukset sekä listan raidoista ja kirjoittaa JSON-tiedoston ```json.dump()``` komennolla.

Sekvenssin lataaminen JSON-tiedostosta tekee samat askeleet käänteisessä järjestyksessä sillä erotuksella, että ladatusta sekvenssidatasta luodaan uudet ```Track``` oliot luokkametodilla ```load_track_from_file()``` ja nämä syötetään uuteen ```sequence```olioon.
