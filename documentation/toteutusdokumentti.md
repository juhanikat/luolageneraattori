# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelman käynnistyessä se näyttää käyttäjälle graafisen käyttöliittymän, jossa käyttäjä voi päättää esimerkiksi huoneiden määrän, huoneiden minimi- ja maksimikoon ja kartan koon.
Kun käyttäjä painaa Run-nappia, ohjelma ensiksi generoi kartalle käyttäjän määrittelemän määrän huoneita.
Sen jälkeen tiedostossa services/generate.py oleva funktio käyttää projektissa olevia algoritmeja (tiedostossa algorithms.py) luodakseen huoneiden väliset käytävät.
Lopuksi ohjelma näyttää luodun kartan käyttäjälle matplotlib-kirjaston tekemän graafin kautta. Käytävät yhdistyvät huoneiden vasempaan alakulmaan. Ohjelman käyttöliittymään ja graafin piirtämiseen liittyvä koodi on ui/ui.py tiedostossa.

## Aikavaativuudet

- Bowyer-Watsonin algoritmin aikavaativuus on O(n^2)
- Kruskalin algoritmin aikavaativuus on O(E log E), jossa E on kaarien määrä.
- A\* algoritmin aikavaativuus on O(b^d), jossa b on keskimääräinen polkujen määrä yhdestä solmusta (tämän ohjelman tapauksessa 4) ja d on lyhimmän polun pituus.

## Puutteet

- Generoidut käytävät ovat välillä täydellisen suoria, joka ei välttämättä vastaa mielikuvaa luolastosta.
- Ohjelman käyttämä reitinhakualgoritmi on liian hidas suurilla kartoilla. Esimerkiksi 1000x1000 kokoisen kartan generoiminen kestää käytännössä ikuisesti.
- Jos kartan koko on liian pieni, ohjelma voi epäonnistua asettamaan huoneet kartalle jolloin se ilmoittaa tästä virheviestillä käyttäjälle. Tämä johtuu siitä että ohjelma kokeilee asettaa huoneita eri puolille karttaa satunnaisesti, ja lopettaa yrittämisen tietyn epäonnistumisten määrän jälkeen. Tämä on ärsyttävää käyttäjälle, eikä ole selvää kuinka suuri kartta käyttäjän täytyy luoda että huoneet mahtuvat kartalle.
- Ohjelmalla menee joskus kauan asettaa huoneita kartalle edellisen kohdan toiminnan takia, esimerkiksi jos kartta on liian pieni.

## Apuvälineet

Projektissa olevan Kruskalin algoritmin, UnionFind-luokan ja reitinhakualgoritmin tekemiseen on käytetty TIRA 2024 kevät-kurssin materiaaleja. Projektissa ei ole käytetty ChatGPT:tä tai muita laajoja kielimalleja.
