+++
title = "Time Machine: UUID of disk changed"
slug = "time-machine-volume-uuid"
date = "2011-02-18T15:00:47Z"
bestbefore = "2021-03-11"
aliases = [
  "/hints/macosx/time-machine-volume-uuid/",
  "/articles/time-machine-volume-uuid/"
]
categories = [ "macOS" ]
tags = [ "macOS" ]
disqusurl = "https://simon.heimlicher.com/articles/2011/02/18/time-machine-volume-uuid"
summary = "If you clone a volume that you backup with Time Machine, its UUID will change and Time Machine will no longer be able to back it up. Use the following script to change the UUID of the existing backups, leading Time Machine to backup as if the volume's UUID had never changed"
thumbnail = "images/thumbnail"
featureImage = "images/Time Machine - UUID of disk changed"
+++

If you clone a volume that you backup with Time Machine, its UUID will change and Time Machine will no longer be able to make backups of it. However, it won't tell you directly what the problem is. Rather, you will find entries like the following in `/var/log/system.log`:
	
``` plain
backupd Backup failed with error: 12
backupd Error (12): Link of previous volume failed for macosx.
```


If you want to continue to backup to the same volume in your Time Machine backup database, the following script allows you to change the UUID of the existing backups, leading Time Machine to backup as if the volume's UUID had never changed.


{{% note update %}}
Starting from OS X Lion 10.7, there is a nifty new command line utility called `tmutil`, which takes care of the task previously accomplished by the script described below. Here is an example of how to [use `tmutil` to associate a new disk with an existing backup](/articles/time-machine-inherit-backup-using-tmutil).
{{% /note %}}

## Usage Example

{{< responsive-code lang="bash" title="Example usage" >}}
./timemachine-setuuid.sh "Backup of MyMac" "Macintosh HD"
	
Using Time Machine volume
  "/Volumes/Backup of MyMac"
with backup database located at
  "/Volumes/Backup of MyMac/Backups.backupdb/MyMac"
	
UUID of volume "Macintosh HD" will be set to "394FBC68-AA00-3556-81B5-D61F5BFA27ED"
	
Done
{{< /responsive-code >}}

## Script

And here's the script. 

{{< responsive-code lang="bash" title="Shell script `timemachine-setuuid.sh`" >}}
#!/usr/bin/env bash
set -u; set -e
	
# From: http://www.macosxhints.com/article.php?story=20090213071015789
# All credits go to the author "only_solutions ()". Their profile is at
# http://www.macosxhints.com/users.php?mode=profile&uid=1060791
	
if [[ $# -ne 2 ]]; then
    echo "Usage: `basename "$0"` `<Time Machine volume, e.g. \"Backup of My Mac\">` `<Disk whose UUID needs to be set, e.g. \"Macintosh HD\">`"
		exit 1
fi
	
errxit () {
    [[ "$2" ]] && printf "$2\n" >&2
    exit ${1:-1}
}
	
say () {
    msg="${1-`}"
    [[ ! -z "$msg" ]] && printf "$msg\n" >&2
}
	
# Check if Time Machine volume is mounted in /Volumes
TMV="$( cd "/Volumes/$1" && pwd )"
	
# Check if source volume is mounted in /Volumes
SRCVOLUME="$( cd "/Volumes/$2" && pwd )"
	
# Strip '/Volumes' to obtain source volume name
VOLNAME="${SRCVOLUME#/Volumes/}"
	
# Get source volume UUID
UUID="$( diskutil info "$SRCVOLUME" | sed -nE 's/.*Volume UUID: +([-A-F0-9]+).*/\1/p' )"
	
# Get path to backup database
BDB="$TMV/Backups.backupdb/$(scutil --get ComputerName)"
if ! ls "$BDB" &>/dev/null; then
    errxit 1 "Invalid backup database path:
  \"$BDB\""
fi
	
if ! ls "$BDB/"*/"$VOLNAME" &>/dev/null; then
    errxit 1 "Volume \"$VOLNAME\" not found in backup database at
  \"$BDB\""
fi
	
say "Using Time Machine volume
  \"$TMV\"
with backup database located at
  \"$BDB\"
	
UUID of volume \"$VOLNAME\" will be set to \"$UUID\"
"
	
# Disable ACL protection on Time Machine volume
sudo fsaclctl -p "$TMV" -d
	
sudo xattr -w com.apple.backupd.SnapshotVolumeUUID "$UUID" \
    "$BDB"/[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]-*/"$VOLNAME"
	
# Re-enable ACL protection on Time Machine volume
sudo fsaclctl -p "$TMV" -e
	
echo "Done"
{{< /responsive-code >}}

Save the above code to a file called e.g. `timemachine-setuuid.sh` and make that file executable by issuing

``` bash
chmod +x "timemachine-setuuid.sh"
```

