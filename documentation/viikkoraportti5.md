# Viikkoraportti 5

Käytetty aika: 11h

Vaihdoin Dijkstran algoritmin a\*- algoritmiin, joka paransi sen suorituskykyä kartan kokoa kasvatettaessa. Algoritmi on silti hidas noin 500x500 kokoisella tai isommalla kartalla. Aika ei riittänyt huoneiden generoimisen ja asettelemisen paranteluun, joten ne laitetaan vieläkin kutakuinkin satunnaisesti kartalle.

Ongelmia tuotti se, että triangulaatioalgoritmi ei tuota oikeaa tulosta jos 3 huonetta ovat suunnilleen samassa linjassa keskenään. Pyrin ratkaisemaan ongelman ensi viikolla.

Seuraavalla viikolla pyrin myös parantamaan testejä, dokumentaatiota ja koodin yleisasua.
