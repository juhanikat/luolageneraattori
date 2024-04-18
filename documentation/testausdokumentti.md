# Testausdokumentti

Testit voidaan ajaa suorittamalla komento `poetry run invoke test` projektin juurikansiossa.

Algoritmeja:

- Bowyer-Watsonin algoritmia on testattu muun muassa varmistamalla, että kolme huonetta muodostaa aina keskenään kolmion, paitsi jos kaikki huoneet ovat samalla x- tai y-koordinaatilla. Tällä hetkellä algoritmi toimii tarpeeksi nopeasti tuhannella huoneella, mutta 10 000 on jo hidas. Vaikka tämä on riittävä suorituskyky tälle ohjelmalle, pyrin katsomaan myöhemmin voiko algoritmia optimoida lisää.
- Virittävää puuta testataan varmistamalla että kolmen huoneen välinen kolmio muuttuu kahdeksi poluksi, ja neljän uoneen välinen suorakulmio muuttuu kolmeksi poluksi. Lisäksi varmistetaan, ettei lineaarinen polku muutu miksikään, koska sellainen algoritmin on tarkoitus tuottaa.
- A\*- ja Dijkstran algoritmia testataan varmistamalla, että ne laskevat lyhyimmän reitin pituuden kartalla jossa ei ole mitään, sekä kartalla jossa reitin tiellä on huoneita.
- Room-luokkaa testataan varmistamalla että huoneen pinta-ala kerrotaan oikein ja että luokan get_all_coords() metodi antaa kaikki huoneen peittämät koordinaatit.
- Map-luokkaa testataan muun muassa varmistamalla että place_rooms() metodille ei voi antaa vääränlaisia argumentteja, ja että luokan metodit lisäävät huoneet oikein luokan tietorakenteisiin.

Algoritmien yhteistoimintaa testataan tiedostossa test_generate.py varmistamalla, että generate.py:ssä sijaitseva funktio muodostaa luolaston oikein.

## Yksikkötestauksen kattavuusraportti

```
============================= 21 passed in 57.68s ==============================
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/algorithms.py            158      4     70      6    96%   152, 192->222, 197, 223, 264->294, 295
src/entities/cell.py           6      0      0      0   100%
src/entities/geometry.py      55      5      2      1    89%   21, 24, 54, 77, 148
src/entities/hallway.py        3      0      0      0   100%
src/entities/map.py          116     10     50      5    90%   96, 104, 107, 110, 232-239
src/entities/room.py          20      1      6      0    96%   42
src/services/generate.py      46      4     16      2    84%   44, 58-61
src/utilities.py              25      9      8      0    61%   33-41
----------------------------------------------------------------------
TOTAL                        429     33    152     14    90%
```
