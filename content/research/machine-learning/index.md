---
date: "2012-12-11T15:39:01Z"
description: Using machine learning to enable movie recommendations without the users having to exchange their personal ratings of the movies
image:
  feature: images/robynne-hu-HOrhCnQsxnQ-unsplash-original
  thumbnail: images/robynne-hu-HOrhCnQsxnQ-unsplash-square
lastmod: "2023-03-16T17:58:36.115Z"
title: Machine learning
weight: 100
---

At Technicolor, we designed and evaluated a distributed inference algorithm to provide recommendations for media such as movies or TV shows

Thanks to the [Netflix Prize](https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data) data set, we had ample material to evaluate our algorithm with. 
As opposed to the objective of the Netflix Prize, however, our goal was to offer provable privacy guarantees to all users. 
To accomplish this, we relied on two core tools. 
First, [belief propagation](https://en.wikipedia.org/wiki/Belief_propagation) on Bayesian networks allowed us to *distribute* computations. 
Second, [differential privacy](https://en.wikipedia.org/wiki/Differential_Privacy) provided the provable privacy guarantees we were looking for. 
Differential privacy was originally developed at Microsoft Research; more recently, [Apple has picked up differential privacy](https://machinelearning.apple.com/research/learning-with-privacy-at-scale) as a research focus.

## Selected publications

Simon Heimlicher, Marc Lelarge, Laurent Massoulié:   
**Community Detection in the Labelled Stochastic Block Model**   
NIPS 2012 Workshop: Algorithmic and Statistical Approaches for Large Social Networks, Lake Tahoe, Nevada.
[Paper as PDF](/research/publications/heimlicher_community-labelled-sbm_nips12.pdf)

Please refer to the [complete list of publications](/research/publications/) for further information.

----
Photo by <a href="https://unsplash.com/@robynnexy">Robynne Hu</a> on <a href="https://unsplash.com/photos/HOrhCnQsxnQ">Unsplash</a>
