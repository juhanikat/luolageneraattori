# Testausdokumentti

Testit voidaan ajaa suorittamalla komento `poetry run invoke test` projektin juurikansiossa.

Algoritmeja:

- Bowyer-Watsonin algoritmia on testattu muun muassa varmistamalla, että kolme huonetta muodostaa aina keskenään kolmion, paitsi jos kaikki huoneet ovat samalla x- tai y-koordinaatilla.
- Kruskalin algoritmia testataan varmistamalla että se luo polut oikein. Lisäksi varmistetaan, ettei lineaarinen polku muutu miksikään, koska sellainen algoritmin on tarkoitus tuottaa.
- A\*- ja Dijkstran algoritmia testataan varmistamalla, että ne laskevat lyhyimmän reitin pituuden kartalla jossa ei ole mitään, sekä kartalla jossa reitin tiellä on huoneita.
- Room-luokkaa testataan varmistamalla että huoneen pinta-ala kerrotaan oikein ja että luokan get_all_coords() metodi antaa kaikki huoneen peittämät koordinaatit.
- Map-luokkaa testataan muun muassa varmistamalla että luokan metodit lisäävät huoneet oikein luokan tietorakenteisiin, ja että konstruktorille ei voi antaa vääränlaisia parametrejä.

Algoritmien yhteistoimintaa testataan tiedostossa test_generate.py varmistamalla, että generate.py:ssä sijaitseva funktio muodostaa luolaston oikein ja että muodostuvassa luolastossa on oikea määrä käytäviä.

## Yksikkötestauksen kattavuusraportti

```
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/algorithms.py            123      2     56      3    97%   130, 193->223, 224
src/entities/cell.py           6      0      0      0   100%
src/entities/geometry.py      58      5      2      1    90%   31, 34, 64, 88, 158
src/entities/hallway.py        3      0      0      0   100%
src/entities/map.py          120     10     52      5    90%   112, 120, 123, 126, 257-264
src/entities/room.py          17      1      4      0    95%   38
src/services/generate.py      50      4     18      2    85%   59, 77-80
src/values.py                  7      0      0      0   100%
----------------------------------------------------------------------
TOTAL                        384     22    132     11    92%
```
