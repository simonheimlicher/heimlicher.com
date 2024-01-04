---
date: "2012-01-29T04:21:00Z"
image:
  feature: images/ferdinand-stohr-nKg8IsVFMV8-unsplash
  thumbnail: images/ferdinand-stohr-nKg8IsVFMV8-unsplash-square
lastmod: "2023-03-18T16:44:06.415Z"
summary: A methodology and its empirical validation based on GPS traces from taxi cabs that characterizes mobile networks via the size of clusters of connected nodes
title: Characterizing mobile wireless networks
weight: 500
---

Are all computers in a network always able to communicate with each other? Yes, at least when we consider the Internet or your home Wi-Fi. However, when we study communication among mobile devices carried by people, this assumption no longer holds. We have developed a methodology to characterize such networks. The initial publication received the award for the best paper at the *ACM MobiHoc* conference, a top-tier conference for mobile networking, in 2010.

Depending on the range of the wireless communication link, the mobility of the nodes and environmental factors such as buildings shadowing the signal, only some of the nodes might be able to communicate with each other at any instant in time.

Therefore, networks can be classified based on the *connectivity* of their physical link topology.

Connected

: a network is called *connected* if it permanently provides paths between all nodes.

Disconnected

: Otherwise, it is referred to as *disconnected*. 

Partially connected

: If a disconnected network provides physical paths between a sizable fraction of nodes, we say it is *partially connected,* as opposed to a scenario where all nodes are isolated almost all the time. 

To optimally use the opportunities provided by a network for communication between any pair of nodes, it is imperative to understand the characteristics of its link topology.

## Prior approaches to describe connected and disconnected networks

Two methodologies have been used in prior work to characterize networks. Initially, [percolation theory](https://en.wikipedia.org/wiki/Percolation_theory) has enjoyed broad interest. More recently, in the realm of [delay-tolerant networking (DTN)](https://en.wikipedia.org/wiki/Delay-tolerant_networking), the stochastic process describing contacts, i.e., short encounters between nodes, has gained significant traction. Under the lens of percolation theory, the conditions required for a certain degree of connectivity can be studied, while in delay-tolerant networks, the focus is on opportunistically using contacts for forwarding. The broad literature in these domains notwithstanding, neither of those methodologies adequately describes the whole gamut of mobile wireless networks.

{{< responsive-image resource="images/observed-vs-predicted-merge-split-ratio-square_transparent" caption="Comparison of the observed vs. the predicted ratio between merge and split rate" background="light" lightbox="true" >}}

## Characterizing arbitrarily connected mobile wireless networks

We have developed a methodology to characterize arbitrary mobile wireless network scenarios via the distribution of the size of connected components (clusters) in the physical link topology. To derive this distribution, we model the network as a [Markov process](https://en.wikipedia.org/wiki/Markov_process) describing the sizes of clusters evolving through merge and split reactions between clusters. The parameters of this process are estimated based on the observable statistics of merge and split reactions of a given scenario. The stationary state of the process is obtained analytically and characterizes the physical connectivity provided by the scenario. Further, we show that for an increasing number of nodes, the behavior of the process converges to a mean-field behavior and we derive a simple, closed-form approximation describing the expected cluster size distribution. This is remarkable as it provides a simple relationship between the microscopic statistics of merge and split events between clusters and the resulting macroscopic cluster size distribution. Indeed, because the process also captures the temporal behavior of the scenario, we are able to predict the fluctuation of the cluster size of an individual node over time. We validate these theoretical results against several synthetic and real-world contact and mobility traces with dozens to thousands of nodes, confirming the validity of the model and showing remarkable accuracy of the predicted behavior.

{{< responsive-image resource="images/empirical-validation-shanghai-taxicabs_transparent" caption="Empirical validation against GPS location traces from taxi cabs in Shanghai" background="light" lightbox="true" >}}

Simon Heimlicher and Kavé Salamatian:  
**Globs in the Primordial Soup — The Emergence of Connected Crowds in Mobile Wireless Networks**  
ACM MobiHoc 2010, Chicago, September 2010.  
**★ Best Paper Award ★**   
[Paper as PDF](/research/publications/heimlicher_globs_mobihoc10.pdf) | [Extended Version as PDF](/research/publications/heimlicher_globs_mobihoc10-extended.pdf)

---
Photo by <a href="https://unsplash.com/fr/@fellowferdi?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Ferdinand Stöhr</a> on <a href="https://unsplash.com/photos/nKg8IsVFMV8?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
