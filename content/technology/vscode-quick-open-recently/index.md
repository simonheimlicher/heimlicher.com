---
categories:
- VSCode
date: "2023-09-09T08:12:30Z"
description: VSCode allows opening recent files quickly but they are not ordered by recency. This setting changes that
draft: false
featured: false
image:
  feature: images/vscode-quick-open-settings-recency
tags:
- VSCode
- Settings
title: "VSCode: Order files in Quick Open by recency"
---


*VSCode* offers a practical menu to quickly open files that have been opened recently or that are found in the current workspace based on typing a few characters of the file name.

You can open this file by hitting <kbd>⌘-P</kbd> on your Mac or <kbd>Ctrl-P</kbd> on Windows and Linux.

{{< responsive-image caption="By default, VSCode lists recently opened files alphabetically" resource="images/vscode-quick-open-settings-default" float=right relative-width=40 lightbox=true  >}}

## Using the VSCode UI

You can change this setting from the default value of `default` to `recency`.

{{< responsive-image caption="By changing the value of `search.quickOpen.history.filterSortOrder` to `recency`, we get VSCode to list recently opened files by recency" resource="images/vscode-quick-open-settings-recency" float=right relative-width=40 lightbox=true >}}

1. Type <kbd>⌘-K</kbd> on your Mac or <kbd>Ctrl-K</kbd> on Windows and Linux
2. Enter `Search:Quick Open:History:Filter Sort Order` into the search field
3. Use the dropdown menu beneath *Controls sorting order of editor history in quick open when filtering* and set it to *recency*.

## Editing the `settings.json` file

If you prefer to edit the `settings.json` directly, add the key–value pair `search.quickOpen.history.filterSortOrder` and set it to `recency` under the root-level key `settings`,

### Example: Change workspace settings

You can also add the below snippet to your workspace or folder settings.

{{< responsive-code lang="json" title="Save this as `project.code-workspace`" >}}
"settings": {
    "search.quickOpen.history.filterSortOrder": "recency"
}
{{< /responsive-code >}}

This setting was introduced via this [feature request on GitHub](https://github.com/microsoft/vscode/issues/35610) regarding the inconsistent ordering of recently opened files in the  *Quick Open* menu. I have no idea why the VSCode developers decided to keep the default setting other than *backward compatibility*.
