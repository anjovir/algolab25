## Mitä olen tehnyt tällä viikolla?
- päivittänyt trie-rakenteen hyödyntäen sanakirjaa, mikä mahdollistaa nyt nuottien kestojen ja taukojen lisäämisen trie-rakenteeseen
- päivittänyt metodin, jossa generoitu midi-sekvenssi tallennetaan kovalevylle. Tämä mahdollistaa myös taukojen kirjoittamisen


## Miten ohjelma on edistynyt?
- ohjelma edistyy, nyt täytyy hioa käyttöliittymän bugeja pois ja alkaa testaamaan enemmän

## Mitä opin tällä viikolla / tänään?
- trie-rakenteen rakentaminen hyödyntäen sanakirjaa
- Markovin ketjuejen hyödyntäminen rytmin generoimiseen
- midon hyödyntäminen midi-tiedoston tallentamisessa
- (yksikkö)testaamista

## Mikä jäi epäselväksi tai tuottanut vaikeuksia?
- testannut eri tapoja sisällyttää rytmi sekvenssiin. Alkuperäinen tapa, jossa nuottisekvenssit ja rytmit generoitiin erikseen (jälkimmäinen perustuen kokonaisiin tahteihin ja miten ne seuraavat toisiaan) ei toiminut ja tulos ei tyydyttänyt
- nyt tehty metodi, jossa nuotit ja niiden kestot tallennetaan samaan trie-rakenteeseen tuottaa parempia tuloksia, vaikkakaan melodiat eivät noudata tahtien kestoja.
-midi_player-luokan testaus on ollut hankalaa ja olen tässä opetellut mock-kirjaston käyttöä, missä tosin vielä hahmotettavaa

## Käytetty tuntimäärä
- 18

## Mitä teen seuraavaksi?
- testausta
- metodi midi-kappaleen käsittelyyn, jotta siitä saadaan melodia irti syötedataksi manuaalisen käsittelyn sijasta.
- käyttöliittymän hiomista
- generoituja nuottiketjuja voisi hioa siten, että se noudattaisi selkeämmin jotain tahtilajia - mikäli ehdin
