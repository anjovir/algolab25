## Mitä olen tehnyt tällä viikolla?
- nuottien syöttäminen trie-rakenteeseen ja tämän toimivuuden tarkistus
- nuottien generointi
- käyttöliittymän rakentaminen
- testaamisen perusteet
- rytmien lukeminen midi-tiedostosta

## Miten ohjelma on edistynyt?
- trie-rakenne näyttäisi nyt toimivan, samoin nuottisekvenssin generointi perustuen eri pituisiin Markovin ketjuihin
- olen rakentanut yksinkertaisen käyttöliittymän ohjelmallee eri parametrien säätämiseen
- metodi uuden kappaleen lataamiseen trie-rakenteeseen täytyy uudistaa

## Mitä opin tällä viikolla / tänään?
- trie-rakenteen käytännön toteutus 
- trie-rakenteeen ja Markovin ketjun yhdistäminen ja nuottien generoiminen perustuen kappaleessa esiintyvään sekvenssiin
- syötedatan uniikkien sekvenssien hakeminen trie-rakenteesta ja listaaminen
- pygamen hyödyntäminen midi-soittimena melodian soittamiseen
- yksikkötestaamista (minimaalisessa määrin)
- midi-tiedoston nuottien ja taukojen lukeminen mido-kirjastolla

## Mikä jäi epäselväksi tai tuottanut vaikeuksia?
- trie-rakenne näyttäisi olevan nyt kunnossa, mutta tämän tarkasteluun voisi vielä luoda erillisen metodin
- pitkällisen vääntämisen jälkeen midolla sain nuottien ja taukojen kestot pääteltyä kahdesta esimerkkitiedostosta. Ongelmana midi-viestien järjestyksen hahmottaminen ja nuottien kestojen sisältyminen eri tyyppisiin midi-viesteihin (time signature, note_on, note_off, pitchwheel), minkä selvittäminen vaati paljon testaamista ja tutkimista. Voi olla että jotain caseja jäi vielä ulkopuolelle, mutta ne täytyy tarkistaa myöhemmin
- tämän toteuttamisessa meni pidemmän aikaa kuin piti, joten tämän datan vieminen trie-rakenteeseen jää ensi viikolle
- ylimääräisen mutkan tässä aiheutti music21-jonka note.Rest-toiminnon piti tarjota tähän nopea ratkaisu alun perin, mutta lopulta kirjasto tuotti midi-tiedoston lukemisessa anomalioita, joiden korjaaminen osoittautui vielä työläämmäksi kuin mido-kirjastolla tuotettu ratkaisu, jolloin tämä työ täytyi heittää roskiin. Osan siitä onneksi pystyi hyödyntämään konseptitasolla midoa hyödyntävän metodin kirjoittamiseen.

## Käytetty tuntimäärä
- 33

## Mitä teen seuraavaksi?
- testausta
- Markovin ketjun hyödyntäminen melodian rytmin generoimiseksi. Nyt tyydyn ratkaisuun, jossa rytmi generoidaan nuoteista erillisinä täyden tahdin mittaisina sekvensseinä. Tämän vieminen trie-rakenteeseen vaatii vielä hiukan pohdintaa.
- metodi midi-kappaleen käsittelyyn, jotta siitä saadaan melodia irti syötedataksi manuaalisen käsittelyn sijasta
- käyttöliittymän hiomista