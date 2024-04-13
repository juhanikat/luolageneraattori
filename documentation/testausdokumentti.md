# Testausdokumentti

Testit voidaan ajaa suorittamalla komento `poetry run invoke test` projektin juurikansiossa.

Algoritmeja:

- Bowyer-Watsonin algoritmia on testattu muun muassa varmistamalla, että kolme huonetta muodostaa aina keskenään kolmion, paitsi jos kaikki huoneet ovat samalla x- tai y-koordinaatilla. Tällä hetkellä algoritmi toimii tarpeeksi nopeasti tuhannella huoneella, mutta 10 000 on jo hidas. Vaikka tämä on riittävä suorituskyky tälle ohjelmalle, pyrin katsomaan myöhemmin voiko algoritmia optimoida lisää.
- Virittävää puuta testataan varmistamalla että kolmen huoneen välinen kolmio muuttuu kahdeksi poluksi, ja neljän uoneen välinen suorakulmio muuttuu kolmeksi poluksi. Lisäksi varmistetaan, ettei lineaarinen polku muutu miksikään, koska sellainen algoritmin on tarkoitus tuottaa.
- Room-luokkaa testataan varmistamalla että huoneen pinta-ala kerrotaan oikein ja että luokan get_all_coords() metodi antaa kaikki huoneen peittämät koordinaatit.
- Map-luokkaa testataan muun muassa varmistamalla että place_rooms() metodille ei voi antaa vääränlaisia argumentteja.

Algoritmien yhteistoimintaa testataan tiedostossa test_generate.py varmistamalla, että generate.py:ssä sijaitseva funktio muodostaa luolaston oikein.

## Yksikkötestauksen kattavuusraportti

```
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/algorithms.py             99      3     48      3    96%   128, 171, 197
src/entities/cell.py           6      0      0      0   100%
src/entities/geometry.py      53      4      2      1    91%   21, 51, 74, 145
src/entities/hallway.py        3      0      0      0   100%
src/entities/map.py          100      8     46      3    91%   75, 78, 81, 218-222
src/entities/room.py          20      1      6      0    96%   42
src/services/generate.py      37      3     10      1    83%   42-45
src/testing.py               131    131     50      0     0%   1-173
src/utilities.py              19      9      6      0    48%   30-38
----------------------------------------------------------------------
TOTAL                        468    159    168      8    64%
```
