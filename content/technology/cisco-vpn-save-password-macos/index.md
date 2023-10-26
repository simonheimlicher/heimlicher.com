---
aliases:
- /hints/macosx/cisco_vpn/
- /articles/cisco-vpn/
- /articles/cisco-vpn-save-password-macos/
# Article has been updated to indicate its end of life
bestBefore: "9999-07-26"
categories:
- macos
date: "2011-03-17"
lastmod:  "2016-03-17"
disqusurl: https://simon.heimlicher.com/articles/2011/03/17/cisco-vpn
slug: cisco-vpn-save-password-macos
summary: 'Snow Leopard brought built-in support for Cisco VPN over TCP (but not over
  UDP). However, as of 10.6.6, there is still one issue: While the password can be
  saved in the keychain, the daemon `configd` is not granted access, causing the user
  to be bothered to enter the password every time upon initiating a connection'
tags:
- macos
title: Save Password of Cisco VPN in Mac OS X 10.6
---

{{% note important %}}
This hint only applies to versions of Mac OS X up to version 10.8 Mountain Lion.
{{% /note %}}

Snow Leopard brought built-in support for Cisco VPN over TCP (but not over UDP). However, as of 10.6.6, there is still one issue: While the password can be saved in the keychain, the daemon `configd` is not granted access, causing the user to be bothered to enter the password every time upon initiating a connection.

If you are running Mac OS X 10.6.0–10.6.3 and experience unexpected disconnections when the phase 1 key should be renegotiated (after 48 minutes), [there is a work-around here](/technology/fix-cisco-vpn-disconnections-mac-os-x-10.6.0-10.6.3/).

The password issue can be solved as follows

 1. Open "Keychain Access" (use Spotlight)
 2. Find the entry corresponding to the `XAUTH` password using the search field
 3. Click the "Access Control" tab, then the "+" button and add `/usr/libexec/configd` to the list of applications that are allowed to access the keychain entries. To navigate to this directory, just start typing `/usr/libexec/` and then select `configd`.

{{% note important %}}

Common problems

* Whenever you change the slightest detail of your VPN configuration, you will have to do this again.
* If you are still being asked for your password when using the VPN menu item to initiate a connection, try disabling and subsequently re-enabling  the VPN menu ("Show VPN status in menu bar"), then repeat the above.
* If you get an error message about a "configuration problem" when initiating the connection, it is typically due to `racoon` being running when it should not be. To kill this daemon, proceed as follows:
  * Be sure to be logged in as administrator.
  * Open the "Terminal" application
  * Type `sudo killall racoon` and press the "Return" key
  * When asked for a password, enter your login password.

{{% /note %}}

{{< responsive-image caption="Navigating to `/usr/libexec/configd`" resource="images/navigate_to_configd.png" >}}

{{< responsive-image caption="Successfully added `/usr/libexec/configd`'" resource="images/configd_added.png" >}}
