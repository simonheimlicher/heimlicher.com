---
aliases:
- /articles/time-machine-inherit-backup-using-tmutil/
bestbefore: "2025-02-11"
categories:
- macos
date: "2012-07-10T18:35:00Z"
description: How to use the terminal command `tmutil` to force Time Machine to continue
  the backup history of the previous disk with your new Mac or a new internal disk
image:
  excerpt:
    alt: Screenshot of the man page of tmutil, a macOS command to manage Time Machine
      backups
    src: images/associate-disk-with-tmutil_excerpt
    title: Associate Time Machine disk with your new Mac
  feature:
    alt: Screenshot of the man page of tmutil, a macOS command to manage Time Machine
      backups
    position: top left
    src: images/associate-disk-with-tmutil_feature
    title: Associate Time Machine disk with your new Mac
lastmod: "2023-04-24T12:47:01Z"
slug: time-machine-inherit-backup-using-tmutil
summary: In situations where macOS does not associate your Time Machine backup disk
  to your new Mac or a new internal disk automatically, `tmutil` lets you force Time
  Machine to continue the backup history of the previous disk
tags:
- macos
title: 'Time Machine: Inherit Backup Using `tmutil`'
---

You plug in your Time Machine disk and your Mac asks out of the blue a question you did not expect: would you like your Mac to *inherit the backup history on the disk,* or *start a new backup?*

 Why did Time Machine ask this question? And how come it has never asked this question before? Time Machine uses a unique ID (`UUID`) that is specific to the disk in your Mac to associate it with its backup. In general, the stubborness of Time Machine is meant to prevent data loss in cases such as when a different disk with the same name is attached to your Mac. Thanks to the different `UUID`, Time Machine detects that this is in fact not the same physical disk and will not add a new snapshot to the backup history of your own volume.

Nonetheless, there are a few cases, where this is exactly what we want.

You might also have made the painful experience that Time Machine silently started a new backup history when you expected it to continue the one it had been working on for years.

Apple has documented the most popular situations; please refer to the support article corresponding to your version of macOS:

* [macOS 10.13 *High Sierra*](https://support.apple.com/guide/mac-help/a-mac-inherit-backup-history-mh35732/10.13/mac/10.13)
* [macOS 10.14 *Mojave*](https://support.apple.com/guide/mac-help/if-your-new-mac-inherits-your-backup-history-mh35732/10.14/mac/10.14)
* [macOS 10.15 *Catalina*](https://support.apple.com/guide/mac-help/if-your-new-mac-inherits-your-backup-history-mh35732/10.15/mac/10.15)
* [macOS 11.0 *Big Sur*](https://support.apple.com/guide/mac-help/if-your-new-mac-inherits-your-backup-history-mh35732/11.0/mac/11.0)
* [macOS 12 *Monterey*](https://support.apple.com/guide/mac-help/if-your-new-mac-inherits-your-backup-history-mh35732/12.0/mac/12.0)
* [macOS 13 *Ventura*](https://support.apple.com/guide/mac-help/if-your-new-mac-inherits-your-backup-history-mh35732/13.0/mac/13.0)

If these articles do not answer your question or you would like to understand in more detail, how Time Machine associates disks with a Mac and how it decides, when it asks you if you want to inherit the backup history, read on.

## A typical example

Let's say the hard drive of your clunky old MacBook is called `Macintosh HD` the MacBook is called `John Doe's MacBook`, and it is backed up to an external disk called `Time Machine Disk`. In this case, the backing store (`Machine Store` in `tmutil`  lingo) of your MacBook is at `/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook` and the latest backup of `Macintosh HD` is at `/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook/Latest/Macintosh HD`. 

Now you migrate to a blazing fast new SSD, but for sake of simplicity, you still call it `Macintosh HD` because you erase and sell your old hard disk.

After the migration, Time Machine thinks that you have a completely new disk and will start a fresh backup. In the process, it will likely erase almost all of your existing backups to make space.

That's certainly not what you want. You would like Time Machine to simply inherit the existing backups in order to be able to browse those old backups in the future and possibly restore some files. Moreover, instead of creating an entirely new full backup from your admittedly brand new disk, future backups should just be added as incremental backups to the existing backup history.

 ## Manual mode: `tmutil`

To accomplish the above feat, running a single command with `tmutil` is sufficient.

In versions of macOS before the now ancient *OS X 10.7 Lion,* when people exchanged their disk or migrated to a different Mac, this feature has made it difficult to get Time Machine to continue adding to the backup history of the previously used disk. Since OS X Lion, there is a nifty Terminal command called `tmutil`, which provides complete control over the situation.

The most popular use case will be when you migrate your data to a new volume, either on the same disk or a different disk, or a new logic board or a different machine, and you know that you will not be taking any more backups of the previous volume.

In those cases, it can be desirable to associate the new volume with your backup history.

## Using `tmutil` to associate an existing Time Machine backup with your new computer or disk

{{% note  %}}
The following command permanently manipulates the association of your Time Machine disk. Use it only once you understand what this means. You proceed at your own risk.

Please make sure you understand what this does and read the `man` page of `tmutil` (run `man tmutil` in Terminal).
{{% /note %}}

Here is the description of the `verb` `associatedisk`, which we will use for this purpose:

``` plain
associatedisk mount_point snapshot_volume
    Bind a volume store directory to the specified local disk,
    thereby reconfiguring the backup history. Requires root and Full
    Disk Access privileges.

    In Mac OS X, HFS+ and APFS volumes have a persistent UUID that is
    assigned when the file system is created. Time Machine uses this
    identifier to make an association between a source volume and a
    volume store. Erasing the source volume creates a new file system
    on the disk, and the previous UUID is not retained. The new UUID
    causes the source volume -> volume store association to be
    broken. If one were just erasing the volume and starting over, it
    would likely be of no real consequence, and the new UUID would
    not be a concern; when erasing a volume in order to clone another
    volume to it, recreating the association may be desired.

[...]
```

Note that the notation `[-a]` in the man page indicates that `-a` is an optional parameter: The -a option tells associatedisk to find all snapshot volumes in the same machine directory that match the identity of `snapshot_volume`, and then perform the association on all of them. This means either of the following are correct, depending on your needs.

### Associate all snapshots (what you normally want)

In general, you want to associate the entire backup history from a previous computer or disk with your new one. This is accomplished with the following command. Note that we add `-a` immediately after the verb `associatedisk`:

``` plain
sudo tmutil associatedisk -a "/Volumes/Macintosh HD" "/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook/Latest/Macintosh HD"
```

### Only associate a single snapshot

In case you only want to access a single backup from a specific snapshot, for example the most recent one, you can run `tmutil associatedisk` without the `-a` option.

``` plain
sudo tmutil associatedisk "/Volumes/Macintosh HD" "/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook/Latest/Macintosh HD"
```

You will probably be prompted to enter a password. Type you regular macOS administrator password you use to log in to your computer. The characters you type won't be displayed, that's to be expected.

### Expected result

Again quoting from the `man` page:

``` plain
    The result of the above command would associate the volume store
    MyStuff in the specified backup with the source volume
    MyNewStuffDisk. The volume store would also be renamed to match.
    The -a option tells associatedisk to find all volume stores in
    the same machine directory that match the identity of MyStuff,
    and then perform the association on all of them.
```
