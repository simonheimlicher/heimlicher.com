---
date: "2012-01-29T04:21:00Z"
image:
  feature: images/4973677407_aaef445b5b_o
  thumbnail: images/4973677407_aaef445b5b_o-square
lastmod: "2023-03-18T16:44:28.292Z"
summary: On leveraging partial connectivity for multi-hop forwarding in mobile networks
title: Forwarding paradigms in mobile wireless networks
weight: 600
---

Research abounds on how to communicate in networks that are either almost always connected or where links between nodes only appear sporadically. In contrast, to leverage opportunities from partial paths has not been investitgated in any comparable depth.

Having found that even in disconnected network scenarios, [multi-hop paths exist](../characterizing-networks), we compare analytically the performance of two basic paradigms for end-to-end forwarding in a wireless network scenario. As a baseline, we use **source forwarding,** which halts transmission if no end-to-end paths is available, corresponding to classical end-to-end transport protocols. As an obvious alternative, we consider **intermediate forwarding,** which continues forwarding data toward the destination even during disruption periods. While intermediate forwarding mimics the behavior of the standard ad hoc routing protocols (DSR and AODV), perhaps surprisingly, intermediate forwarding is not unconditionally superior.

{{< claris/render-image src="images/partially-connected-networks_transparent" caption="*Partially-connected* networks (grey areas) are situated between *connected* (black) and *disconnected* networks (white)" background="light" lightbox="true" >}}

## Impact of Mobility

We model the forwarding of a packet as a Markov chain whose states correspond to the remaining number of hops to the destination; forwarding and mobility are implemented by moving packets closer to or further from the destination. Even if we assume either of two well-known stochastic relationships between the path length before and after the disruption, intermediate forwarding is not guaranteed to be superior. Therefore we introduce a new criterion based on stochastic dominance which leads to the expected result of superiority. We provide strong evidence that the criterion holds in simple models; whether it holds for a real-world scenario at hand depends on the mobility pattern and the employed routing algorithm.

Simon Heimlicher, Merkouris Karaliopoulos, Hanoch Levy and Thrasyvoulos Spyropoulos:  
**On Leveraging Partial Paths in Partially-connected Networks**  
IEEE INFOCOM 2009, Rio de Janeiro, April 2009.  
[Paper as PDF](/research/publications/heimlicher_partialpaths_infocom09.pdf)

## Impact of the Loss Process

Further, a similar model can be used to investigate the impact of correlation in the loss process. As with the impact of mobility, the loss process may lead to surprising results. We compare analytically the performance of retransmission from the source node **(end-to-end transport)** with per-hop retransmission **(hop-by-hop transport)**. We show that basic per-hop retransmission, which naturally has a very small round-trip time, may be inferior to end-to-end retransmission if the loss process is positively correlated. However, if the per-hop algorithm is parametrized so as to use the same retransmission intervals as end-to-end retransmission **(spaced hop-by-hop)**, it is superior for any form of correlation in the loss process.

Simon Heimlicher and Bernhard Plattner:  
**Reliable Transport in Multi-hop Wireless Mesh Networks**  
Book: [Guide to Wireless Mesh Networks](https://link.springer.com/book/10.1007/978-1-84800-909-7?detailsPage=toc)  
Series: Computer Communications and Networks  
Misra, Sudip; Misra, Subhas Chandra; Woungang, Isaac (Eds.), January 2009  
ISBN (Print): `978-1-84800-908-0`  
ISBN (Online): `978-1-84800-909-7`  
DOI: `10.1007/978-1-84800-909-7_9`  
Chapter available at [Springer Online](https://link.springer.com/chapter/10.1007/978-1-84800-909-7_9)

Simon Heimlicher, Merkouris Karaliopoulos, Hanoch Levy and Martin May:  
**End-to-end vs. Hop-by-hop Transport under Intermittent Connectivity** (Invited Paper)  
ICST Autonomics 2007, Rome, Italy, October 2007.  
[Paper as PDF](/research/publications/heimlicher_e2e-vs-hbh-intermittent_autonomics07.pdf)

Simon Heimlicher, Pavan Nuggehalli and Martin May:  
**End-to-end vs. Hop-by-hop Transport**  
ACM International Conference on Measurement and Modeling of Computer Systems, ACM SIGMETRICS 2007, Student Workshop, San Diego, CA, USA, June 2007.  
[Paper as PDF](/research/publications/heimlicher_e2e-vs-hbh-transport_sigmetrics07.pdf)

## SAFT, a Hop-by-Hop Transport Protocol

To investigate the feasibility of intermediate forwarding or hop-by-hop transport, we have developed **SAFT (store-and-forward transport)** a hop-by-hop transport protocol for mobile wireless networks that uses AODV to determine the next hop and continues forwarding toward the destination for a given period of tim if the end-to-end path may be disrupted. As compared to classical TCP over AODV, SAFT provides up to a three times shorter end-to-end delay.

Simon Heimlicher, Rainer Baumann, Martin May, Bernhard Plattner:  
**The Transport Layer Revisited**  
2nd IEEE International Conference on Communication System Software and Middleware, IEEE COMSWARE 2007, Bangalore, India, January, 2007.  
[Paper as PDF](/research/publications/heimlicher_transport-layer-revisited_comsware07.pdf)

Simon Heimlicher, Rainer Baumann, Martin May, Bernhard Plattner:  
**SaFT: Reliable Transport in Mobile Networks**  
3rd IEEE International Conference on Mobile Ad-hoc and Sensor Systems, IEEE MASS 2006, Vancouver B.C., Canada, pages 477-480, October, 2006.  
[Paper as PDF](/research/publications/heimlicher_saft_mass06.pdf)
