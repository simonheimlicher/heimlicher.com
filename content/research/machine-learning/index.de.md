---
date: "2023-03-12T13:20:20Z"
description: Nutzung von Maschinellem Lernen, um Empfehlungen für Filme zu generieren, ohne dass die Nutzenden ihre persönlichen Bewertungen der Filme austauschen müssen
image:
  feature: 
    resource: images/robynne-hu-HOrhCnQsxnQ-unsplash-original
    credit: '<a href="https://unsplash.com/@robinne">Robynne Hu</a> on <a href="https://unsplash.com/photos/HOrhCnQsxnQ">Unsplash</a>'
    alt: Eine Gruppe von Menschen, die beieinander stehen  
  thumbnail: images/robynne-hu-HOrhCnQsxnQ-unsplash-square
lastmod: "2023-03-16T17:58:36.115Z"
title: Maschinelles Lernen
weight: 100
---

Bei Technicolor haben wir ein verteiltes Empfehlungssystem entwickelt und evaluiert, um Empfehlungen für Medien wie Filme oder Fernsehsendungen zu generieren.

Dank des Datensatzes des [Netflix Prize](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data) hatten wir genügend Daten, um unser Empfehlungssystems zu evaluieren. Im Gegensatz zum Netflix Prize war es jedoch nicht nur das Ziel, eine möglichst gute Empfehlung abzugeben, sondern gleichzeitig den Nutzern des Empfehlungssystems nachweisbare Garantien bezüglich der Wahrung Ihrer Privatsphäre zu bieten.

Um dies zu erreichen, haben wir uns auf zwei Kernwerkzeuge verlassen:

1. Wir verwendeten [Belief Propagation](https://en.wikipedia.org/wiki/Belief_propagation) in Bayesian Networks, um die für die Empfehlungen notwendigen Berechnungen *zu verteilen*.
2. Wir nutzten [Differential Privacy](https://de.wikipedia.org/wiki/Differential_Privacy), um die Wahrung der Privatspähre beweisbar gewährleisten zu können.

Die differenzielle Privatsphäre wurde ursprünglich bei Microsoft Research entwickelt; in jüngerer Zeit hat [Apple die differenzielle Privatsphäre](https://machinelearning.apple.com/research/learning-with-privacy-at-scale) als Forschungsschwerpunkt übernommen.

## Ausgewählte Publikationen

Simon Heimlicher, Marc Lelarge, Laurent Massoulié:
**Community Detection in the Labelled Stochastic Block Model**
NIPS 2012 Workshop: Algorithmic and Statistical Approaches for Large Social Networks, Lake Tahoe, Nevada.
[Paper als PDF](/research/publications/heimlicher_community-labelled-sbm_nips12.pdf)

Siehe auch die [vollständige Liste der Publikationen](/research/publications/).

----

Foto von <a href="https://unsplash.com/@robinne">Robynne Hu</a> auf <a href="https://unsplash.com/photos/HOrhCnQsxnQ">Unsplash</a>
