# Toteutusdokumentti

## Ohjelman yleisrakenne

Ohjelman käynnistyessä se näyttää käyttäjälle graafisen käyttöliittymän, jossa käyttäjä voi päättää esimerkiksi huoneiden määrän, huoneiden minimi- ja maksimikoon ja kartan koon.
Kun käyttäjä painaa Run-nappia, ohjelma ensiksi generoi kartalle käyttäjän määrittelemän määrän huoneita.
Sen jälkeen tiedostossa services/generate.py oleva funktio käyttää projektissa olevia algoritmeja (tiedostossa algorithms.py) luodakseen huoneiden väliset käytävät.
Lopuksi ohjelma näyttää luodun kartan käyttäjälle matplotlib-kirjaston tekemän graafin kautta. Käytävät yhdistyvät huoneiden vasempaan alakulmaan. Ohjelman käyttöliittymään ja graafin piirtämiseen liittyvä koodi on ui/ui.py tiedostossa.

## Puutteet

Generoidut käytävät ovat usein täydellisen suoria, joka ei välttämättä vastaa mielikuvaa luolastosta. Ohjelman käyttämä reitinhakualgoritmi on myös liian hidas suurilla kartoilla.

## Apuvälineet

Projektissa olevan Spanning Tree-algoritmin ja Dijkstran algoritmin tekemiseen on käytetty TIRA 2024 kevät-kurssin materiaaleja. Projektissa ei ole käytetty ChatGPT:tä tai muita laajoja kielimalleja.
