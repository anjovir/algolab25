# Markovin ketjuja hyödyntävä melodiageneraattori
Sovelluksella voi generoida melodioita perustuen syötteeksi annettuun midi-tiedostoon
- tässä vaiheessa midi-tiedosto tulisi olla siistitty seuraavalla tavalla:
    1. Vain yksi midi-kanava tulisi olla jäljellä, jonka sisältönä tulisi olla yksinuottisia melodioita

## Sovelluksen käynnistäminen
- Asenna ensin poetryn riippuvuudet komennolla poetry install
- Tämän jälkeen käynnistä sovellus komennolla poetry run invoke start

## Testaus
- Testit voi ajaa komennolla poetry run invoke test
- Testikattavuusraportin saa komennolla poetry run invoke coverage-report

## Pylint
- Tarkistuksen voi tehdä .pylintrc-määritysten mukaisesti komennolla poetry run invoke lint