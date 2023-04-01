+++
title = "Workaround for disconnections of Cisco VPN in Mac OS X 10.6"
slug = "fix-cisco-vpn-disconnections-mac-os-x-10.6.0-10.6.3"
date = "2011-03-17T09:25:23Z"
aliases = [
  "/hints/macosx/cisco_vpn-10.6.0-3/",
  "/articles/cisco-vpn-10.6.0-3/",
  "/articles/fix-cisco-vpn-disconnections-mac-os-x-10.6.0-10.6.3/",
  "/articles/cisco-vpn-10.6/"
]
bestBefore = "2017-06-12"
categories = [ "macOS" ]
tags = [ "macOS" ]
disqusurl = "https://simon.heimlicher.com/articles/2011/03/17/cisco-vpn-10.6.0-3"
summary = "The built-in Cisco VPN client introduced in Mac OS X 10.6 Snow Leopard has the habit of disconnecting itself when re-keying should be performed but fails after about 48 minutes up to one hour. This timeout issue has been fixed in Mac OS X 10.6.4"
+++

The built-in Cisco VPN client introduced in Mac OS X 10.6 Snow Leopard has the habit of disconnecting itself when re-keying should be performed but fails after about 48 minutes up to one hour. This timeout issue has been fixed in Mac OS X 10.6.4.

In versions of Mac OS X 10.6.0 up to 10.6.3, the problem can be worked around by increasing the re-keying period to e.g. 1 week. 

{{% note tip %}}
The update to Snow Leopard 10.6.4 fixes the issue of the VPN disconnecting after 48 minutes many people have observed in 10.6.0–10.6.3. Therefore, there is no need to change the configuration of `racoon` anymore.

In order to revert your configuration to the stock one, remove the last line from `/etc/racoon.conf`, so that the last line is again

``` plain
include "/var/run/racoon/*.conf" ;
```
{{% /note %}}

**Note that this workaround severely decreases the security of your VPN connection as attackers now have up to 1 week to attack the phase 1 key**.

I have no clue where Apple stores the configuration template for `racoon`, but I have found the following workaround.

1. Create directory "/etc/racoon/remote" as root:

``` plain
sudo mkdir /etc/racoon/remote
```

2. Open a VPN connection to your Cisco VPN concentrator. This should result in the creation of a config file located at `/var/run/racoon/10.1.1.1.conf`, where `10.1.1.1` is the IP address of the VPN concentrator.

3. Move this dynamically created file to `/etc/racoon/remote` before we change its contents:

``` plain
sudo mv /var/run/racoon/*.conf /etc/racoon/remote
```


4. Now we edit the file, replacing all lines

``` plain
lifetime time 3600 sec;
```
by

``` plain
lifetime time 168 hours;
```

This is achieved by the following `sed` command:

``` plain
sudo sed -i.bak 's/lifetime time 3600 sec/lifetime time 168 hours/' /etc/racoon/remote/*.conf
```

1. To make `racoon` read our converted file, insert a line

``` plain
include "/etc/racoon/remote/*.conf" ;
```
right before the last line of `/etc/racoon.conf`. The last two lines should now be

``` plain
include "/etc/racoon/remote/*.conf" ;
include "/var/run/racoon/*.conf" ;
```
This is achieved by executing the following patch command:
``` plain
sudo patch /etc/racoon/racoon.conf <<EOF
--- /etc/racoon.orig/racoon.conf	2009-06-23 09:09:08.000000000 +0200
+++ /etc/racoon/racoon.conf	2009-12-11 13:52:11.000000000 +0100
@@ -135,4 +135,5 @@
 # by including all files matching /var/run/racoon/*.conf
 # This line should be added at the end of the racoon.conf file
 # so that settings such as timer values will be appropriately applied.
+include "/etc/racoon/remote/*.conf" ;
 include "/var/run/racoon/*.conf" ;
EOF
```

1. Restart racoon:

``` plain
sudo launchctl stop com.apple.racoon
sudo launchctl start com.apple.racoon
```

That's it. If this did not do the trick, try restarting your machine.

To summarize, here are all the commands to be executed:

``` bash
sudo mkdir /etc/racoon/remote
sudo mv /var/run/racoon/*.conf /etc/racoon/remote
sudo sed -i.bak 's/lifetime time 3600 sec/lifetime time 168 hours/' /etc/racoon/remote/*.conf
sudo patch /etc/racoon/racoon.conf <<EOF
--- /etc/racoon.orig/racoon.conf	2009-06-23 09:09:08.000000000 +0200
+++ /etc/racoon/racoon.conf	2009-12-11 13:52:11.000000000 +0100
@@ -135,4 +135,5 @@
	# by including all files matching /var/run/racoon/*.conf
	# This line should be added at the end of the racoon.conf file
	# so that settings such as timer values will be appropriately applied.
+include "/etc/racoon/remote/*.conf" ;
	include "/var/run/racoon/*.conf" ;
EOF
sudo launchctl stop com.apple.racoon
sudo launchctl start com.apple.racoon
```


