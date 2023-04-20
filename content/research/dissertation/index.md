+++
title = "Ph.D. dissertation"
slug = "dissertation"
date = "2010-11-23T17:44:14Z"
alias = "publications/dissertation"
description = "Ph.D. dissertation of Simon Heimlicher entitled “Wireless Communication Among Mobile Nodes: From Paths to Clusters to Connectivity”"
lastmod = "2023-03-16T21:05:55.258Z"
weight = 900
[image]
  feature = "images/dissertation-front"
  thumbnail = "images/dissertation-front"
+++



During my Ph.D. at [ETH Zurich](https://www.ethz.ch), I studied human mobility and the characteristics of the communication opportunities if we assume wireless links between people within close proximity.

Today, it may seem foreign to study situations where no cellular network coverage is available. However, in such situations, communication may be even more important than in the comfort of our daily life as city dwellers. As I have focused on fundamental research, the results from my dissertation can be applied broadly. Indeed, the mathematical model we employ in the first part has been around for over a century and was originally published in a scientific publication in German. My dissertation compmrises two parts, where the first characterizes the scenarios upon which the second is based.

1. The first part coomprises an analytical model for the [**emergence of connected clusters**](characterizing-networks/index.md)) mobile wireless network scenarios. You can imagine these scenarios to be people living in a city that carry a smartphone that is able to connect to all other people within a fixed radius. We were able to validate the accuracy of our model based on traces from people visiting a conference as well as people riding taxi cabs in San Francisco and Shanghai.
2. The second part offers an analytical comparison of paradigms to [**leverage these communication opportunities**](forwarding-paradigms/index.md) for end-to-end communication between two arbitrary people. This analyis was novel as it was the first to explicitly consider the connected crowds predicted by the model introduced in the first part of the dissertation.

## Wireless Communication Among Mobile Nodes: <br/>From Paths to Clusters to Connectivity

Defense: October 4, 2010.

## Ph.D. Committee ##

Prof. Dr. **[Bernhard Plattner](https://ee.ethz.ch/the-department/faculty/emeriti-professors/contact-details.Nzc3OTY=.TGlzdC8xODc5LC05MjU0NzU1MDE=.html)**

Prof. Dr. **[Jim Kurose](https://gaia.cs.umass.edu/personnel/kurose.html)** — University of Massachusetts, USA

Prof. Dr. **[Kavé Salamatian](https://www.univ-smb.fr/listic/en/presentation_listic/membres/enseignants-chercheurs/kave-salamatian/)** — Université de Savoie, France

Prof. Dr. **[Hanoch Levy](https://english.tau.ac.il/profile/hanoch)** — Tel-Aviv University, Israel

### Abstract

A network is essentially a set of nodes connected by physical links, over which logical connections are established to serve the target application.
In classical wired networks, an optimal end-to-end path, i.e. a sequence of links from the source to the destination node, is determined by the routing algorithm.
However, in mobile wireless networks, such end-to-end paths may only be available intermittently.
Indeed, connectivity may be so sparse that communication is only possible by forwarding data along multiple partial paths, each of them bridging a part of the gap between source and destination and thus enabling communication over the course of time.
Establishing and maintaining logical connections over partial paths is a challenging problem to solve in practical implementations and largely determines not only the logical structure of the network but also the performance of applications.
	
Understanding the statistics of those paths is therefore of tremendous practical interest.
One may coarsely classify networks based on connectivity of the entire network: a network is called connected if it permanently provides paths between all nodes, otherwise it is called disconnected.
Disconnected network scenarios may further be distinguished by the extent to which nodes are connected by paths: if a network provides paths between a sizable fraction of nodes, it may be seen as partially connected, as opposed to a scenario where all nodes are isolated almost all the time.
Once the statistics of paths and the requirements of the target application are known, the maximum extent of logical connectivity that may be achieved is of further interest.
But even with a firm grasp on the behavior of paths and the limits of logical connectivity in the target scenario, establishing logical connections over intermittently available paths remains a challenging problem due to the uncertainty inherent in the future topology of the network.

We begin by studying the characteristics of mobile wireless networks in the first part of this dissertation.
We propose a methodology to derive analytically the limits of physical connectivity as a function of the observable statistics of physical links in the target scenario.
We describe physical connectivity through the distribution of the size of connected components, or clusters, in the physical link topology.
Specifically, we model the network as a Markov process describing the sizes of clusters evolving through merge and split reactions among each other.

From the stationary state of this process, we obtain analytically the limits of physical connectivity  as manifested by the cluster size distribution. 
Moreover, we show that with increasing number of nodes, the process tends to a mean field behavior, which allows us to derive a mean field approximation (MFA), i.e. a closed-form expression approximating the cluster size distribution.
Based on the MFA, further predictions can be made, such as the future size of the cluster of a randomly picked node conditioned on its current size.
Thereafter, we model as an example of the composition of logical connections an opportunistic forwarding algorithm and study the attained level of logical connectivity as a function of buffer management at intermediate nodes.
Following this analysis of the stationary behavior, we analyze the transient from isolated nodes to the stationary, which yields a characteristic time scale of the dynamics of the network scenario.
We validate all results against several synthetic and real-world contact and mobility traces with dozens to several thousand nodes. For all traces, we find good agreement of the behavior predicted by the model with the observed behavior of the trace.

Having seen that many mobile wireless network scenarios are neither connected nor consisting of only isolated nodes, we then turn our focus to investigate how to maintain logical connections over intermittently available partial paths in the physical link topology.
In particular, in the second part, we compare analytically the performance of two forwarding paradigms.
As a baseline, we use a paradigm we call source forwarding. This paradigm allows communication only when an end-to-end path is available, corresponding to a classical end-to-end transport protocol.
As an alternative, we consider intermediate forwarding, which continually forwards data closer to the destination along the shortest available path.

We model a connection as a Markov chain whose states correspond to the remaining number of hops to the destination on the shortest path; forwarding and mobility are implemented by moving packets closer to or further from the destination.
Due to mobility, intermediate forwarding is not unconditionally superior.
Indeed, after a disruption, the remaining number of hops from a former intermediate node to the destination may be greater than from the source node.
We study several well-known stochastic relationships between the path length before and after the disruption; however, none of them proves sufficient to guarantee superiority of intermediate forwarding.
We then introduce a criterion based on stochastic dominance, leading to the expected result of superiority, and provide strong evidence that the criterion holds in simple models. Whether the criterion holds in a given scenario depends on the employed routing algorithm and thus needs to be determined individually.

We complement the analysis of the impact of node mobility by analyzing the effect of the link loss process. To this end, we adapt the above model and introduce a two-state link model for every hop along the path, allowing us to adjust the link success probability and the duration of link outages independently. We derive analytically the probability that a packet is delivered successfully requiring no more than a given number of attempts for both forwarding paradigms. Further, we derive the expected number of transmissions at the link layer performed per packet. Perhaps surprisingly, even though the path length is constant in this model, depending on the scheduling of retransmissions, intermediate forwarding is not necessarily superior. Nonetheless, we show that intermediate forwarding deterministically dominates source forwarding if both paradigms use the same scheduling of retransmissions.


