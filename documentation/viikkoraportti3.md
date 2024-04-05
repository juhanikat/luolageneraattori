# Viikkoraportti 3

Lisäsin projektiin graafisen käyttöliittymän tkinter-kirjaston avulla. Lisäsin myös spanning-tree algoritmin, jonka avulla Bowyer-Watsonin algoritmin luomasta triangulaatiosta karsitaan polkuja pois niin, että jokaisessa huoneessa käydään vain kerran. Lopuksi satunnaisesti valittuja pois karsittuja polkuja lisätään takaisin, jotta lopputulos näyttäisi luonnollisemmalta. Refaktoroin myös koodia etenkin algorithms.py moduulissa.

Opin muun muassa virittävä puu-algoritmin toteutuksesta. Vaikeuksia tuotti kolmioiden generoiminen algoritmeja varten, kunnes tajusin että kolmion pisteet olivat välillä suorassa linjassa keskenään, jolloin niitä ei voi tietenkään yhdistää kolmioksi.

Seuraavaksi pyrin korvaamaan ohjelman generoimat suorat viivat ruudukolle asetetuilla neliöillä, jotta ne näyttävät enemmän käytäviltä.
