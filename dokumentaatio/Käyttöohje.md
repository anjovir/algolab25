## Sovelluksen käynnistäminen
- Asenna ensin poetryn riippuvuudet komennolla poetry install
- Tämän jälkeen käynnistä sovellus komennolla poetry run invoke start

## Midi-tiedoston lataaminen ja trie-rakenteen resetointi
- Hae oikean muotoinen midi-tiedosto haluamastasi kansiosta painamalla "Open midi file" -nappia
- Lataa tiedosto trie-rakenteeseen painamalla "Read file"
- Voit myös ladata tietyn tiedostokansion suoraan tietorakenteeseen painamalla "Open directory"
- Jokainen lataus lisää tiedostot trie-rakenteeseen. Trien voi resetoida painamalla "Reset trie" -nappia
- Voit myös kasvattaa trie-rakenteeseen ladattavan nuottiketjun pituutta valitsemalla "Order (trie)"

## Melodian generoiminen
- Valitse ensin, kummalla periaatteella haluat generoida melodian:
1. Nuotit ja rytmit käsitetään yhtenä yksikkönä ("Notes and rhythm considered as an unit")
2. Nuotit ja rytmi generoidaan erikseen ("Notes and rhythm generated separately")
- Valitse sen jälkeen Markovin ketjun aste liukuvalinnasta ("Order (song)")
- aseta tempo (Set tempo)
- aseta nuottiketjun pituus ("Song lenght") (nuotteina, jos valitsit 1., tahteina jos valitsit 2.)
- generoi aloitussekvenssi ("Generate starting sequence")
- valitse generoi kappaleen nuotit ("Generate song notes")

## Midi-tiedoston soittaminen
- valitse avattava tiedosto napista "Open midi file"
- paina nappia "Play"
- keskeytä soittaminen napista "Stop"

##
- Alhaalla näkyy aloitussekvenssi ja kappaleen nuotit midi-viesteinä (sävelkorkeus ja kesto) sekä tahteina,
mikäli on valittuna ehto 2

## Rajoituksia syötteessä
Sovelluksella voi generoida melodioita perustuen syötteeksi annettuun midi-tiedostoon
- tässä vaiheessa midi-tiedosto tulisi olla siistitty seuraavalla tavalla:
    1. Vain yksi midi-kanava tulisi olla jäljellä, jonka sisältönä tulisi olla yksinuottisia melodioita
- Lisäksi minkä tahansa midi-tiedoston lukeminen ei onnistu tällä ohjelmalla, vaikka kyse olisi yksinuottisista melodioista
- tunnistettu puute on nuotit, jotka alkavat toisesta tahdista ja jatkuvat toiseen tahtiin, mikä aiheuttaa ongelmia
generointitavalle 2.