---
categories:
- VSCode
date: "2023-09-09T08:12:30Z"
description: VSCode ermöglicht das schnelle Öffnen von kürzlich verwendeten Dateien, aber diese sind nicht nach Aktualität sortiert. Diese Einstellung ändert das.
draft: false
featured: false
image:
  feature: images/vscode-quick-open-settings-recency
tags:
- VSCode
- Settings
title: "VSCode: Dateien im Schnellöffnen-Menü nach Aktualität sortieren"
---

## Das *Schnellöffnen*-Menü in VSCode

*VSCode* verfügt über ein nützliches Menü, um Dateien, die kürzlich geöffnet wurden oder sich im aktuellen Arbeitsbereich befinden, anhand einiger Buchstaben des Dateinamens rasch zu öffnen.

Dieses Menü lässt sich mit <kbd>⌘-P</kbd> auf Ihrem Mac oder <kbd>Ctrl-P</kbd> auf Windows und Linux aufrufen.

{{< responsive-image caption="Standardmässig listet VSCode kürzlich geöffnete Dateien alphabetisch auf" resource="images/vscode-quick-open-settings-default" float=right relative-width=40 lightbox=true  >}}

## Die VSCode-Oberfläche nutzen

Sie können diese Einstellung vom Standardwert `default` auf `recency` ändern.

{{< responsive-image caption="Indem man den Wert von `search.quickOpen.history.filterSortOrder` auf `recency` ändert, listet VSCode kürzlich geöffnete Dateien nach Aktualität auf" resource="images/vscode-quick-open-settings-recency" float=right relative-width=40 lightbox=true >}}

1. Drücken Sie <kbd>⌘-K</kbd> auf Ihrem Mac oder <kbd>Ctrl-K</kbd> auf Windows und Linux.
2. Geben Sie `Search:Quick Open:History:Filter Sort Order` in das Suchfeld ein.
3. Verwenden Sie das Dropdown-Menü unter *Kontrolliert die Sortierreihenfolge des Editor-Verlaufs im Schnellöffnen beim Filtern* und setzen Sie es auf *recency*.

## Die `settings.json`-Datei bearbeiten

Falls Sie die `settings.json` direkt bearbeiten möchten, fügen Sie das Schlüssel-Wert-Paar `search.quickOpen.history.filterSortOrder` hinzu und setzen Sie es unter dem Root-Level-Schlüssel `settings` auf `recency`.

### Beispiel: Arbeitsbereich-Einstellungen ändern

Sie können auch den untenstehenden Ausschnitt zu Ihren Arbeitsbereich- oder Ordner-Einstellungen hinzufügen.

{{< responsive-code lang="json" title="Speichern Sie dies als `project.code-workspace`" >}}
"settings": {
    "search.quickOpen.history.filterSortOrder": "recency"
}
{{< /responsive-code >}}

Diese Einstellung wurde durch diese [Funktionsanfrage auf GitHub](https://github.com/microsoft/vscode/issues/35610) eingeführt, die sich auf die inkonsistente Sortierung kürzlich geöffneter Dateien im *Schnellöffnen*-Menü bezog. Ich weiss nicht, warum die VSCode-Entwickler beschlossen haben, die Standardeinstellung beizubehalten, möglicherweise aus Gründen der *Rückwärtskompatibilität*.
