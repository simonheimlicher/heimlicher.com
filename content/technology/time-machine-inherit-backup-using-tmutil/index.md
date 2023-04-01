+++
title = "Time Machine: Inherit Backup Using `tmutil`"
slug = "time-machine-inherit-backup-using-tmutil"
date = "2012-07-10T18:35:00Z"
lastmod = "2019-02-11T10:12:01Z"
bestbefore = "2021-02-11"
aliases = ["/articles/time-machine-inherit-backup-using-tmutil/"]
categories = ["macOS"]
tags = ["macOS"]
disqusurl = "https://simon.heimlicher.com/articles/2012/07/10/time-machine-inherit-backup-using-tmutil"
summary = "In OS X Lion and Mountain Lion, `tmutil` lets Time Machine continue the backup history of the previous disk"
+++

Time Machine uses a unique ID (`UUID`), which is specific to a volume (i.e. a partition of a disk), to associate the volume with its backup. In OS X releases before 10.7 Lion, when people exchanged their disk or migrated to a different Mac, this feature has made it difficult to get Time Machine to continue adding to the backup history of the previously used disk.

In OS X Lion and now also OS X 10.8 Mountain Lion, there is a nifty new Terminal command called `tmutil`, which makes this whole drama a breeze. In general, the stubborness of Time Machine is meant to prevent data loss in cases such as when a different disk with the same name is attached to your Mac. Thanks to the different `UUID`, Time Machine detects that this is in fact not the same physical disk and will not add a new snapshot to the backup history of your own volume.

Nonetheless, there are a few cases, where this is exactly what we want. 

The most popular use case will be when you migrate your data to a new volume, either on the same disk or a different disk, or even different machine, and you know that you will not be taking any more backups of the previous volume.

In those cases, it can be desirable to associate the new volume with your backup history.

Let's say the hard drive of your clunky old MacBook is called `Macintosh HD` the MacBook is called `John Doe's MacBook`, and it is backed up to an external disk called `Time Machine Disk`. In this case, the backing store (`Machine Store` in `tmutil`  lingo) of your MacBook is at `/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook` and the latest backup of `Macintosh HD` is at `/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook/Latest/Macintosh HD`. 

Now you migrate to a blazing fast new SSD, but for sake of simplicity, you still call it `Macintosh HD` because you erase and sell your old hard disk. 

After the migration, Time Machine thinks that you have a completely new disk and will start a fresh backup. In the process, it will likely erase almost all of your existing backups to make space.

That's certainly not what you want. You would like Time Machine to simply inherit the existing backups in order to be able to browse those old backups in the future and possibly restore some files. Moreover, instead of creating an entirely new full backup from your admittedly brand new disk, future backups should just be added as incremental backups to the existing backup history.

To accomplish this, a single command with `tmutil` is sufficient. 

{{% note  %}}
The following command permanently manipulates the association of your Time Machine disk. Use it only once you understand what this means. You proceed at your own risk.

Please make sure you understand what this does and read the `man` page of `tmutil` (run `man tmutil` in a Terminal).
{{% /note %}}

Here is the description of the `verb` `associatedisk`, which we will use for this purpose:

``` plain
associatedisk [-a] mount_point snapshot_volume
     Bind a snapshot volume directory to the specified local
     disk, thereby reconfiguring the backup history. Requires
     root privileges.
[...]
```

Note that the notation `[-a]` in the man page indicates that `-a` is an optional parameter: The -a option tells associatedisk to find all snapshot volumes in the same machine directory that match the identity of `snapshot_volume`, and then perform the association on all of them. This means either of the following are correct, depending on your needs.

Only associate a single snapshots
``` plain
sudo tmutil associatedisk "/Volumes/Macintosh HD" "/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook/Latest/Macintosh HD"
```


Associate all snapshots (what you normally want):
``` plain
sudo tmutil associatedisk -a "/Volumes/Macintosh HD" "/Volumes/Time Machine Disk/Backups.backupdb/John Doe's MacBook/Latest/Macintosh HD"
```


You will probably be prompted to enter a password. Type you regular OS X login password. The characters you type won't be displayed, that's to be expected.

Again quoting from the `man` page:

``` plain
The result of the above command would associate the snapshot
volume MyStuff in the specified snapshot with the source
volume MyNewStuffDisk. The snapshot volume would also be
renamed to match. The -a option tells associatedisk to find
all snapshot volumes in the same machine directory that
match the identity of MyStuff, and then perform the associa-
tion on all of them.
```

