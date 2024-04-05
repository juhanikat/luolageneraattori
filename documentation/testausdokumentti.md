# Testausdokumentti

Testit voidaan ajaa suorittamalla komento `poetry run invoke test` projektin juurikansiossa.

Algoritmeja:

- Bowyer-Watsonin algoritmia on testattu muun muassa varmistamalla, että kolme huonetta muodostaa aina keskenään kolmion, paitsi jos kaikki huoneet ovat samalla x- tai y-koordinaatilla. Tällä hetkellä algoritmi toimii tarpeeksi nopeasti tuhannella huoneella, mutta 10 000 on jo hidas. Vaikka tämä on riittävä suorituskyky tälle ohjelmalle, pyrin katsomaan myöhemmin voiko algoritmia optimoida lisää.
- Virittävää puuta testataan varmistamalla että kolmen huoneen välinen kolmio muuttuu kahdeksi poluksi, ja neljän uoneen välinen suorakulmio muuttuu kolmeksi poluksi. Lisäksi varmistetaan, ettei lineaarinen polku muutu miksikään, koska sellainen algoritmin on tarkoitus tuottaa.
- Room-luokkaa testataan varmistamalla että huoneen pinta-ala kerrotaan oikein ja että luokan get_all_coords() metodi antaa kaikki huoneen peittämät koordinaatit.
- Map-luokkaa testataan muun muassa varmistamalla että place_rooms() metodille ei voi antaa vääränlaisia argumentteja.

```
Name                   Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------
src/algorithms.py        103      4     32      1    96%   21, 50, 85, 117
src/entities/map.py       75      8     34      3    88%   106, 108, 111, 148-152
src/entities/room.py      20      1      6      0    96%   40
src/utilities.py          60     60     22      0     0%   1-128
------------------------------------------------------------------
TOTAL                    258     73     94      4    71%
```