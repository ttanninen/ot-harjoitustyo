# Arkkitehtuurikuvaus

## Ohjelman rakenne

Ohjelman alustava pakkausrakenne on kuvattu seuraavassa kaaviossa:
\
<img width="50%" alt="sequencer_app drawio" src="https://github.com/user-attachments/assets/42a6418d-464e-4f53-85b1-edecdaa14c52" />
\
Services pakkaus sisältää ohjelman toiminnallisuuden eli äänen toistamisesta ja äänitiedostojen käsittelystä vastaava audioengine.py sekä sekvensserin varsinaisen toimintalogiikan sisältävä sequencer.py

Toimintalogiikka on eriytetty käyttöliittymästä, joka sijaitsee pakkauksessa ui.py. Käyttöliittymä on pyritty luomaan niin, että mitään sovelluksen toiminnallisuutta ei ole toteutettu vain käyttöliittymän pakkauksessa.

Samples hakemistoon voi tallentaa äänitiedostoja niiden helpon löydettävyyden vuoksi. Ohjelma voi kuitenkin avata äänitiedostoja mistä tahansa kansiosta käyttäjän tietokoneella.

## Käyttöliittymä

Sovelluksen käyttöliittymä koostuu yhdestä näkymästä, jossa kaikki sekvensserin toiminnallisuudet ovat nähtävillä. Sekvensseri-ikkunan koko mukautuu dynaamisesti sekvenssin pituuden eli askelten lukumäärän mukaan. 

## Sovelluslogiikka
Sovellus rakentuu app.py moduulin omistamiin Sequencer ja AudioEngine luokkiin, jotka alustetaan index.py -moduulissa ohjelman käynnistyessä. 

Pakkaus audioengine on jaettu luokkiin AudioFile ja AudioEnginen. Näiden luokkien metodit luovat toiminnallisuuden wav-tiedostojen käsittelyyn, sekä monen äänen samanaikaiseen toistamiseen. Äänitiedostojen käsittely ja toisto on toteutettu miniaudio-kirjastolla. Miniaudiolla luodaan jatkuva audio stream, joka lähettää ääntä käyttäjän ensisijaiseen äänilaitteeseen. Äänivirtaan lisätyt äänet toistetaan pienellä (oletus: 15 ms) viiveellä, jotta prosessointi ei vaikuta äänen toistoaikaan.

Pakkaus Sequencer sisältää luokat Track ja Sequence. Käyttäjän luoma sekvenssi rakennetaan muokkaamalla luokan Track-olioita ja lisäämällä niitä luokan Sequence-olioon. Luokka Track sisältää raidalle ladatun äänidatan sekä patternin, jota sekvenssi toistaa. Pattern syötetään listamuodossa, joka muutetaan numpy arrayksi, jossa "0" tarkoittaa tyhjää askelta ja "1" soitettavaa askelta. Track sisältää metodit patternin muokkaamiseen.

Sequencer luokka vastaa varsinaisen sekvensserin toiminnasta looppaamalla Track-olioita läpi ja lähettämällä niiden sisältämiä äänidata tietoja audioenginelle toistoa varten. Sequencer sisältää myös kaikki käyttöliittymälle tarjottavat metodit sekvenssin toistamiseen ja raitojen askelien muokkaamiseen. Sekvenssin asetukset, kuten tempo ja tahtilaji ovat myös muokattavissa käyttöliittymän kautta.

## Päätoiminnallisuudet

Sekvenssikaavio uuden raidan lisäämisestä käyttöliittymän kautta:
<img width="519" height="361" alt="add_track_diag drawio" src="https://github.com/user-attachments/assets/981bc41f-4441-4f15-8e1a-ddfd4f5aedda" />

Sekvenssikaavio play-nappulan painamisesta äänitiedoston toistoon:
<img width="779" height="264" alt="play_sound drawio" src="https://github.com/user-attachments/assets/6cf6bcee-1ac1-4755-98b9-4cc12cba65e1" />

