## Mitä olen tehnyt tällä viikolla?
- päivittänyt trie-rakenteen hyödyntäen sanakirjaa, mikä mahdollistaa nyt nuottien kestojen ja taukojen lisäämisen trie-rakenteeseen
- päivittänyt metodin, jossa generoitu midi-sekvenssi tallennetaan kovalevylle. Tämä mahdollistaa myös taukojen kirjoittamisen


## Miten ohjelma on edistynyt?
- ohjelma edistyy, nyt täytyy hioa käyttöliittymän bugeja pois ja alkaa testaamaan enemmän
- itse ydinongelmassa on vielä paljonkin tekemistä, esim. tauot 

## Mitä opin tällä viikolla / tänään?
- trie-rakenteen rakentaminen hyödyntäen sanakirjaa
- Markovin ketjuejen hyödyntäminen rytmin generoimiseen (paljon hankalampaa pelkkien nuottien generoiminen)
- midon hyödyntäminen midi-tiedoston tallentamisessa
- (yksikkö)testaamista

## Mikä jäi epäselväksi tai tuottanut vaikeuksia?
- testannut eri tapoja sisällyttää rytmi sekvenssiin. Alkuperäinen tapa, jossa nuottisekvenssit ja rytmit generoitiin erikseen (jälkimmäinen perustuen kokonaisiin tahteihin ja miten ne seuraavat toisiaan) ei toiminut ja tuloksena tuli vielä (nykyistäkin) surkeampaa jälkeä
- nyt tehty metodi, jossa nuotit ja niiden kestot tallennetaan samaan trie-rakenteeseen tuottaa parempia tuloksia, mutta kappaleet, joissa on paljon taukoja, aiheuttaa generoidussa kappaleessa sekaisuutta (päällekkäin soivia nuotteja) ja rytmit eivät osu tahteihin - kuitenkin tulos on parempi kuin jos rytmi ja nuottisekvenssi generoitaisiin toisista riippumatta - tässä on työstöä

## Käytetty tuntimäärä
- 5

## Mitä teen seuraavaksi?
- testausta
- täytyy kehittää jokin järkevä, jossa on triehen on tallennettu sekä nuotti, että sen kesto ja saada Markovin ketjun generoimismetodia päivitettyä siten, että saataisiin aikaan täysiä tahtilajeja ja tauot myös selkeytettyä siten, että päällekkäisiä nuotteja soisi nykyisessä määrin
- metodi midi-kappaleen käsittelyyn, jotta siitä saadaan melodia irti syötedataksi manuaalisen käsittelyn sijasta.
- käyttöliittymän hiomista