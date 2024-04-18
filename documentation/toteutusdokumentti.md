# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelman käynnistyessä se näyttää käyttäjälle graafisen käyttöliittymän, jossa käyttäjä voi päättää esimerkiksi huoneiden määrän, huoneiden minimi- ja maksimikoon ja kartan koon.
Kun käyttäjä painaa Run-nappia, ohjelma ensiksi generoi kartalle käyttäjän määrittelemän määrän huoneita.
Sen jälkeen tiedostossa services/generate.py oleva funktio käyttää projektissa olevia algoritmeja (tiedostossa algorithms.py) luodakseen huoneiden väliset käytävät.
Lopuksi ohjelma näyttää luodun kartan käyttäjälle matplotlib-kirjaston tekemän graafin kautta. Käytävät yhdistyvät huoneiden vasempaan alakulmaan. Ohjelman käyttöliittymään ja graafin piirtämiseen liittyvä koodi on ui/ui.py tiedostossa.

## Puutteet

- Generoidut käytävät ovat usein täydellisen suoria, joka ei välttämättä vastaa mielikuvaa luolastosta.
- Ohjelman käyttämä reitinhakualgoritmi on liian hidas suurilla kartoilla. Esimerkiksi 1000x1000 kokoisen kartan generoiminen kestää käytännössä ikuisesti.
- Jos kartan koko on liian pieni, ohjelma voi epäonnistua asettamaan huoneet kartalle jolloin se ilmoittaa tästä virheviestillä käyttäjälle. Tämä johtuu siitä että ohjelma kokeilee asettaa huoneita eri puolille karttaa satunnaisesti, ja lopettaa yrittämisen tietyn epäonnistumisten määrän jälkeen. Tämä on ärsyttävää käyttäjälle, eikä ole selvää kuinka suuri kartta käyttäjän täytyy luoda että huoneet mahtuvat kartalle.

## Apuvälineet

Projektissa olevan Spanning Tree-algoritmin ja Dijkstran algoritmin tekemiseen on käytetty TIRA 2024 kevät-kurssin materiaaleja. Projektissa ei ole käytetty ChatGPT:tä tai muita laajoja kielimalleja.
