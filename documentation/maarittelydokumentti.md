# Määrittelydokumentti

Opinto-ohjelma: tietojenkäsittelytieteen kandidaatti (TKT) 

Projektin kieli on Python. Osaan myös JavaScriptiä.

Aihe: luolastojen generointi 

Aiheeni ydin on luolien generoimiseen käytettävät algoritmit. Käyttäjä antaa ohjelmalle syötteenä kuinka monta huonetta verkostossa tulee olla, kuinka suuria ne ovat ja kuinka iso kartta on. Ohjelma luo satunnaisen verkoston huoneita ja niitä yhdistäviä käytäviä, ja näyttää lopputuloksen selkeästi ohjelman käyttäjälle.

Projektissa toteutettavia algoritmeja ovat muun muassa A*, pienin virittävä puu sekä Bowyer-Watsonin algoritmi. Tavoitteena on, että Bowyer-Watsonin algoritmi toimii O(n^2) ajassa.

Riippuvuksien hallintaan käytän Poetry-työkalua, ja lisäksi käytän mm. Pylint- ja Unittest-kirjastoja koodin oikeellisuuden varmistamiseen ja testaamiseen.

Lähteet ja inspiraatio:
- https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
- https://en.wikipedia.org/wiki/Delaunay_triangulation
- https://vazgriz.com/119/procedurally-generated-dungeons/
- https://www.gorillasun.de/blog/bowyer-watson-algorithm-for-delaunay-triangulation/
