+++
title = "Machine learning"
description = "Machine learning for movie recommendations – preserving privacy"
weight = 100
date = "2023-03-12T13:20:20Z"
lastmod = "2023-03-16T17:58:36.115Z"
[image]
  thumbnail = "images/robynne-hu-HOrhCnQsxnQ-unsplash-square"
  feature = "images/robynne-hu-HOrhCnQsxnQ-unsplash-original"
+++

Bei Technicolor haben wir ein verteiltes Empfehlungssystem entwickelt und evaluiert, um Empfehlungen für Medien wie Filme oder Fernsehsendungen zu generieren.

Dank des Datensatzes des [Netflix Prize](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data) hatten wir genügend Daten, um unser Empfehlungssystems zu evaluieren. Im Gegensatz zum Netflix Prize war es jedoch nicht nur das Ziel, eine möglichst gute Empfehlung abzugeben, sondern gleichzeitig den Nutzern des Empfehlungssystems nachweisbare Garantien bezüglich der Wahrung Ihrer Privatsphäre zu bieten.

Um dies zu erreichen, haben wir uns auf zwei Kernwerkzeuge verlassen:

1. Wir verwendeten [Belief Propagation](https://en.wikipedia.org/wiki/Belief_propagation) in Bayesian Networks, um die für die Empfehlungen notwendigen Berechnungen *zu verteilen*.
2. Wir nutzten [Differential Privacy](https://de.wikipedia.org/wiki/Differential_privacy), um die Wahrung der Privatspähre beweisbar gewährleisten zu können.

Die differenzielle Privatsphäre wurde ursprünglich bei Microsoft Research entwickelt; in jüngerer Zeit hat [Apple die differenzielle Privatsphäre](https://machinelearning.apple.com/2017/12/06/learning-with-privacy-at-scale.html) als Forschungsschwerpunkt übernommen.

## Ausgewählte Publikationen

Simon Heimlicher, Marc Lelarge, Laurent Massoulié:   
**Community Detection in the Labelled Stochastic Block Model**   
NIPS 2012 Workshop: Algorithmic and Statistical Approaches for Large Social Networks, Lake Tahoe, Nevada.   
[<i class="fa fa-file-pdf"></i>&nbsp;Paper als PDF](/research/publications/heimlicher_community-labelled-sbm_nips12.pdf)

Siehe auch die [vollständige Liste der Publikationen](/research/publications/).

----

Foto von <a href="https://unsplash.com/@robynnexy?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Robynne Hu</a> auf <a href="https://unsplash.com/photos/HOrhCnQsxnQ?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
