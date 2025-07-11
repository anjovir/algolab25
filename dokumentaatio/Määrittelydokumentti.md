# Opinto-ohjelma: Tietojenkäsittelytiede, kandidaatin tutkinto (TKT)

# Minkä ongelman ratkaiset eli harjoitustyön ydin
- Tuotan ohjelman, joka generoi melodioita käyttäen eri asteisia Markovin ketjuja, ainakin asteita 1-3.
- Tämän pohjalta syntyy kuva, miten Markovin ketjut toimivat melodioiden tuottamisessa suhteessa alkuperäiseen syöteaineistoon.

# Mitä ohjelmointikieltä käytät?
- Python

# Kerro myös mitä muita kieliä hallitset siinä määrin, että pystyt tarvittaessa vertaisarvioimaan niillä tehtyjä projekteja.
- Osaan arvioida lähinnä Pythonilla kirjoitettua koodia

# Mitä algoritmeja ja tietorakenteita toteutat työssäsi?
- sanakirja, lista, tuple
- Tavoitteena alustavasti on tehdä Markovin ketjuista sanakirja, johon tallennan listana syöteaineistossa esiintyvät kolmen nuotin ketjut ja arvoiksi annan toisen sanakirjan, johon
kirjataan näistä seuraava nuotti ja sen esiintymistiheys.

# Riippuvuudet
- Ohjelmassa musiikin käsittelyyn käytän mm. music21-python kirjastoa

# Mitä syötteitä ohjelma saa ja miten niitä käytetään?
- Syötteitä ohjelma saa midi-muodossa
- Tämän käsittelyyn rakennetaan soveltuva käyttöliittymä. Tarkoituksena on myös analysoida erityisesti melodioita ja sävelkorkeuksia, ei rytmiikkaa.
- Ymmärtääkseni midi-aineisto kannattaa olla yksinuottista aineistoa, jotta saan hyödynnettyä Markovin ketjua seuraavan nuotin generoimiseksi

Tavoitteena olevat aika- ja tilavaativuudet (esim. O-analyysit)
- Tavoitteena on analysoida eri asteisia Markovin ketjuja.
- Tällaisen Markovin ketjun aikavaatimus on luokkaa O(n). Tämä johtuu siitä, että aika kasvaa lineaarisesti syötteenä käytettävien nuottien määrän kasvaessa.
- Tilavaativuus on vakio O(1), mutta koko riippuu Markovin ketjun asteesta. Mitä korkeamman asteen Markovin ketjusta on kyse, sitä suurempi määrä uniikkeja
tiloja tulee tälle varata.
    - Esim. pianossa on 88 kosketinta 12 eri sävelelle useassa eri oktaavissa. Tästä syntyy kolmen nuotin melodioita rajallinen määrä (88^3 = 681 472). 
    - Yleensä musiikissa pysytellään tässä haarukassa. Voidaan myös ajatella, että analysoidaan vain 12 eri sävelen esiintymistä, jolloin päästään lukuun 12^3 = 1728.
    Toisen asteen Markovin ketjussa päästään puolestaan huomattavan pieniin lukuihin.

Lähteet, joita aiot käyttää.
- Aleksi Tarvainen, Markovin ketjut ja Markovin piilomallit algoritmisessa säveltämisessä. Tietotekniikan kandidaatin tutkielma 30.4.2020.
- Miranda Grönlund, Markovin ketjut. Kandidaatin tutkielma 12/2024
- https://en.wikipedia.org/wiki/Mark_V._Shaney
- https://en.wikipedia.org/wiki/Markov_chain


