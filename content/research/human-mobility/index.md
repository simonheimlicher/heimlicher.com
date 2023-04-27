+++
title = "Human mobility"
description = "Human mobility and its impact on network architecture"
date = "2013-02-21T11:21:59Z"
lastmod = "2023-03-18T16:44:38.956Z"
[image]
  feature = "images/human-mobility-feature"
  thumbnail = "images/human-mobility-thumbnail"
+++

The design of a network protocol depends on the assumptions that are made regarding the computers that make up the network. We designed and implemented an Android app to track the mobility of volunteers and correlated their geographic location with the address of their smartphone on the Internet.

The Internet was designed when cellular networks for data were still a few decades out. As a consequence, the architecture of the global network makes a crucial design choice: the address of a computer is tied to its location in the network. This is similar to how phone numbers used to indicate the area by the area code. With the advent of all kinds of wireless technologies, the assumption of fixed nodes no longer holds.

At the [College of Information and Computer Sciences](https://www.cics.umass.edu/) of the [University of Massachusetts (UMass)](https://www.umass.edu/) in Amherst, MA, we studied the mobility of people -- with a twist. Rather than just collecting GPS location data, we compared the trajectory of the *logical* location of the invidiual on the global Internet with their *geographic* location on planet earth. In the **Nomad Log** project to study the mobility of individuals via an Android app named Nomad Log. The results of this study have been published at [SIGCOMM 2014](https://dl.acm.org/doi/10.1145/2619239.2626333).

A visualization of the collected data from my testing in Zurich, Switzerland, is shown below.

{{< responsive-image resource="images/location-transitions_transparent" caption="Mobility traces from the Android app *Nomad Log*" background="light" lightbox="true" >}}

## Selected publications

Zhaoyu Gao, Arun Venkataramani, James F. Kurose, and Simon Heimlicher:   
**Towards a Quantitative Comparison of Location-Independent Network Architectures**   
ACM SIGCOMM 2014, Chicago, August 2014.   
[PDF](/research/publications/gao_netarch_sigcomm14.pdf)

Please refer to the [complete list of publications](/research/publications/) for further information.

----
Photo by <a href="https://unsplash.com/@robynnexy?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Robynne Hu</a> on <a href="https://unsplash.com/photos/HOrhCnQsxnQ?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
