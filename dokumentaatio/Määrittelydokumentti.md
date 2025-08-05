# Opinto-ohjelma: Tietojenkäsittelytiede, kandidaatin tutkinto (TKT)

# Minkä ongelman ratkaiset eli harjoitustyön ydin
- Tuotan ohjelman, joka generoi melodioita käyttäen mielivaltaisia Markovin ketjun asteita
- Tämän pohjalta syntyy kuva, miten Markovin ketjut toimivat melodioiden tuottamisessa suhteessa alkuperäiseen syöteaineistoon.

# Mitä ohjelmointikieltä käytät?
- Python

# Kerro myös mitä muita kieliä hallitset siinä määrin, että pystyt tarvittaessa vertaisarvioimaan niillä tehtyjä projekteja.
- Osaan arvioida lähinnä Pythonilla kirjoitettua koodia

# Mitä algoritmeja ja tietorakenteita toteutat työssäsi?
- Tietorakenteena on trie, johon tallennan nuotit ja niiden frekvenssit
- tätä rakennetta käytän Markovin ketjujen muodostamisessa mielivaltaisella asteella

# Riippuvuudet
- Ohjelmassa musiikin käsittelyyn käytän mm. mido-kirjastoa, pygame.midi-moduulia (midi-toistoon), tkinter-kirjastoa (UI) ym.

# Mitä syötteitä ohjelma saa ja miten niitä käytetään?
- Syötteitä ohjelma saa midi-muodossa
- Tämän käsittelyyn rakennetaan soveltuva käyttöliittymä. Tarkoituksena on myös analysoida erityisesti melodioita ja sävelkorkeuksia, mahdollisesti myös rytmiikkaa
- Ymmärtääkseni midi-aineisto kannattaa olla yksinuottista aineistoa, jotta saan hyödynnettyä Markovin ketjua seuraavan nuotin generoimiseksi

Tavoitteena olevat aika- ja tilavaativuudet (esim. O-analyysit)
- Tavoitteena on analysoida eri asteisia Markovin ketjuja.
- Tällaisen Markovin ketjun aikavaatimus on luokkaa O(n). Tämä johtuu siitä, että aika kasvaa lineaarisesti syötteenä käytettävien nuottien määrän kasvaessa.
- Tilavaativuus on vakio O(1), mutta koko riippuu Markovin ketjun asteesta. Mitä korkeamman asteen Markovin ketjusta on kyse, sitä suurempi määrä uniikkeja
tiloja tulee tälle varata.

Lähteet, joita aiot käyttää.
- Aleksi Tarvainen, Markovin ketjut ja Markovin piilomallit algoritmisessa säveltämisessä. Tietotekniikan kandidaatin tutkielma 30.4.2020.
- Miranda Grönlund, Markovin ketjut. Kandidaatin tutkielma 12/2024
- https://en.wikipedia.org/wiki/Mark_V._Shaney
- https://en.wikipedia.org/wiki/Markov_chain
- https://en.wikipedia.org/wiki/Trie
- https://www.geeksforgeeks.org/dsa/introduction-to-trie-data-structure-and-algorithm-tutorials/



