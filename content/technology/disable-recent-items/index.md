+++
title = "Clear and disable recent items in macOS dock and applications"
slug = "disable-recent-items"
date = "2011-07-26T13:16:58Z"
bestBefore = "2016-07-26"
aliases = ["/hints/macosx/disable_recent_items/", "/articles/disable-recent-items/"]
categories = ["macOS"]
tags = ["macOS"]
disqusurl = "https://simon.heimlicher.com/articles/2011/07/26/disable-recent-items"
summary = "Mac OS X Lion lists recent items with each application in the Dock (accessible via right-click) and in the *Application View* of Mission Control. To remove those and disable future additions, the trusty `defaults write` approach may help with most — but not all — applications"
+++

Mac OS X Lion lists recent items with each application in the Dock (accessible via right-click) and in the *Application View* of Mission Control. To remove those and disable future additions, the trusty `defaults write` approach may help with most — but not all — applications. 

To clear the list of recent files, you need to find the application's bundle identifier. See the next section on how to accomplish this.

Assuming you want to erase the list of recent items in VLC, which has the application bundle identifier `org.videolan.vlc`, you need to issue the following command in Terminal:

``` zsh
defaults delete org.videolan.vlc.LSSharedFileList RecentDocuments
```

To disable listing recent items for VLC in the future, run the following commands in Terminal:
	
``` zsh
defaults write org.videolan.vlc NSRecentDocumentsLimit 0
defaults write org.videolan.vlc.LSSharedFileList RecentDocuments -dict-add MaxAmount 0
```

The same procedure for QuickTime Player X (`com.apple.QuickTimePlayerX`):

``` zsh
defaults delete com.apple.QuickTimePlayerX.LSSharedFileList RecentDocuments
defaults write com.apple.QuickTimePlayerX NSRecentDocumentsLimit 0
defaults write com.apple.QuickTimePlayerX.LSSharedFileList RecentDocuments -dict-add MaxAmount 0
```


After issuing any of the above commands, you need to restart the Dock by issuing

``` zsh
killall Dock
```

That's it.

## Undo
In order to reverse the above modification, you need to again obtain the application's bundle identifier, then run a command in Terminal. As an example, if you should desire to *keep* the list of recent items in VLC (`org.videolan.vlc`), run the following commands in Terminal:
	
	  defaults delete org.videolan.vlc NSRecentDocumentsLimit
  	defaults delete org.videolan.vlc.LSSharedFileList RecentDocuments

For QuickTime Player X (`com.apple.QuickTimePlayerX`), it would be:

``` zsh
defaults delete com.apple.QuickTimePlayerX NSRecentDocumentsLimit
defaults delete com.apple.QuickTimePlayerX.LSSharedFileList RecentDocuments
```

For these commands to take effect, you need to restart the Dock, i.e. issue

``` zsh
killall Dock
```


## Bundle Identifier

In order to figure out the application's bundle identifier, you can either use the Terminal or the Activity Monitor.

If you'd like to go the Terminal route:

1. Open Terminal (use Spotlight if you don't have it in your Dock)
2. type `defaults read` plus a single space character
3. Drag the app into the window to insert its path. If the app is in your Dock, you can **press and hold the ⌘ (command) key** and then grab the app's icon from the Dock and drop it into the Terminal window. Alternatively, you can also grab it from a Finder window and drop it in the Terminal window
4. Now **hit backspace once** to erase the space that was added automatically by the drag-and-drop process
5. Append `/Contents/Info CFBundleIdentifier` (without any preceding space)
6. Finally, hit  ⏎ (the return key) and you should obtain the bundle identifier

For example with Xcode, you would end up with the following command line in Termainal before you hit  ⏎ :

``` zsh
defaults read /Applications/Xcode.app/Contents/Info CFBundleIdentifier
```

Note that you *must not* append the suffix `.plist` to the path above, as this would irritate the `defaults` command.

If this sounds too complicated, you can alternatively open Activity Monitor, click the application in the list of processes and then click the "Sample Process" button. Then make sure the "Display:" popup is set to "Sample Text".

Output for VLC: 

	
``` plain
	Sampling process 66975 for 3 seconds with 1 millisecond of run time between samples
	Sampling completed, processing symbols...
	Analysis of sampling VLC (pid 66975) every 1 millisecond
	Process:         VLC [66975]
	Path:            /Applications/VLC.app/Contents/MacOS/VLC
	Load Address:    0x100000000
	Identifier:      org.videolan.vlc
	Version:         1.1.11 (1.1.11)
	Code Type:       X86-64 (Native)
	Parent Process:  launchd [175]
	[...]
```

Now look for the line that begins with `Identifier:`, which gives you the bundle identifier in plain text. In the above exammple, we find that VLC's application bundle identifier is `org.videolan.vlc`.
