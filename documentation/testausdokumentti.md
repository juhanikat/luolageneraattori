# Testausdokumentti

Testit voidaan ajaa suorittamalla komento `poetry run invoke test` projektin juurikansiossa.

Algoritmeja:

- Bowyer-Watsonin algoritmia on testattu muun muassa varmistamalla, että kolme huonetta muodostaa aina keskenään kolmion, paitsi jos kaikki huoneet ovat samalla x- tai y-koordinaatilla.
- Virittävää puuta testataan varmistamalla että kolmen huoneen välinen kolmio muuttuu kahdeksi poluksi, ja neljän huoneen välinen suorakulmio muuttuu kolmeksi poluksi. Lisäksi varmistetaan, ettei lineaarinen polku muutu miksikään, koska sellainen algoritmin on tarkoitus tuottaa.
- A\*- ja Dijkstran algoritmia testataan varmistamalla, että ne laskevat lyhyimmän reitin pituuden kartalla jossa ei ole mitään, sekä kartalla jossa reitin tiellä on huoneita.
- Room-luokkaa testataan varmistamalla että huoneen pinta-ala kerrotaan oikein ja että luokan get_all_coords() metodi antaa kaikki huoneen peittämät koordinaatit.
- Map-luokkaa testataan muun muassa varmistamalla että luokan metodit lisäävät huoneet oikein luokan tietorakenteisiin, ja että konstruktorille ei voi antaa vääränlaisia parametrejä.

Algoritmien yhteistoimintaa testataan tiedostossa test_generate.py varmistamalla, että generate.py:ssä sijaitseva funktio muodostaa luolaston oikein ja että muodostuvassa luolastossa on oikea määrä käytäviä.

## Yksikkötestauksen kattavuusraportti

```
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/algorithms.py            156      4     70      6    96%   138, 178->208, 183, 209, 250->280, 281
src/entities/cell.py           6      0      0      0   100%
src/entities/geometry.py      55      5      2      1    89%   21, 24, 54, 78, 149
src/entities/hallway.py        3      0      0      0   100%
src/entities/map.py          122     15     54      5    85%   96, 104, 107, 110, 163-172, 252-259
src/entities/room.py          20      1      6      0    96%   42
src/services/generate.py      38      4     16      2    81%   44, 54-57
src/utilities.py              25      9      8      0    61%   33-41
----------------------------------------------------------------------
TOTAL                        425     38    156     14    89%
```
