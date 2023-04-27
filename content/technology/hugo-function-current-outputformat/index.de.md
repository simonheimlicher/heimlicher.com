---
title: Hugo-Funktion, um das aktuelle `OutputFormat` zu erhalten
date: 2023-03-17T07:42:36+01:00
lastmod: 2023-03-20T08:42:44.669Z
description: Hugo bietet derzeit keine Funktion, um das aktuelle OutputFormat zu erhalten - dieses Partial bietet eine einfache Lösung
featured: false
draft: false
# toc: true # Controls if a table of contents should be generated for first-level links automatically.
image:
  feature: images/keith-misner-h0Vxgz5tyXA-unsplash.jpg
# thumbnail: images/thumbnail.png
# shareImage: images/share.png
# codeMaxLines: 10 # Override global value for how many lines within a code block before auto-collapsing.
# codeLineNumbers: false # Override global value for showing of line numbers within code block.
# comment: false # Disable comment if false.
categories:
  - Hugo
tags:
  - Hugo partial
series:
  - Hugo snippets
---

Hugo bietet derzeit keine Funktion, um das aktuelle OutputFormat zu erhalten - dieses *Partial[^1]* bietet eine einfache Lösung.

Hugo ermöglicht das Hinzufügen von [benutzerdefinierten Ausgabeformaten](https://gohugo.io/templates/output-formats/) - jedoch bietet es bis einschließlich Version 0.111.0 keine Funktion, um das `OutputFormat` des aktuellen Seitenkontexts bereitzustellen. Da Hugo zwei Funktionen zur Auflistung verfügbarer `OutputFormat`s bereitstellt, die sich darin unterscheiden, ob sie das aktuelle `OutputFormat` enthalten, liefert ein einfacher Aufruf von [`complement`](https://gohugo.io/functions/complement/) die Antwort.

{{% note %}}
Es gibt ein [offenes Issue auf GitHub](https://github.com/gohugoio/hugo/issues/9368) bezüglich des Fehlens einer `OutputFormat`-Eigenschaft der `Page`-Klasse. [Joe Mooring](https://github.com/jmooring) kam auf dieselbe Lösung wie unten. Aber er fügt auch einen wichtigen Vorbehalt hinzu: Das untenstehende funktioniert nur, solange alle deklarierten `OutputFormat`s folgendes in `config.toml` deklariert haben:

```toml
notAlternative = false
```

{{% /note %}}

Du kannst das folgenden Snippet zu `layouts/partials/_functions` hinzufügen, um diese Funktion in Deinen Templates zu verwenden.

{{< responsive-code lang="go-html-template" title="Speichere dieses Snippet als `layouts/partials/_functions/output-format`" >}}
{{- /* partial output-format
Returns the [OutputFormat](https://gohugo.io/templates/output-formats/)
of the page passed as argument in the current context.
USAGE: use as a function in the context of a page, as follows:
  {{- outputFormat := partial "partials/_functions/output-format" . }}
*/ -}}
{{- $outputFormat := false }}
{{- with (complement $.AlternativeOutputFormats $.OutputFormats) }}
  {{- $outputFormat = index . 0 }}
{{- end }}
{{- return $outputFormat }}
{{< /responsive-code >}}

In diesem Beitrag haben wir gesehen, wie wir mit einem einfachen Partial in Hugo das aktuelle OutputFormat erhalten können, obwohl Hugo selbst noch keine Funktion dafür anbietet. Es ist wichtig zu beachten, dass diese Lösung unter der Bedingung funktioniert, dass alle deklarierten OutputFormats den Parameter `notAlternative = false` in der `config.toml`-Datei deklariert haben.

Durch das Hinzufügen des oben genannten Schnipsels zu `layouts/partials/_functions` kannst Du das OutputFormat in Deinen Templates verwenden und die Ausgabe der Seiten dynamisch anpassen, je nachdem, welches Format gerade verwendet wird.

Denke bitte daran, dass es sich hierbei um eine temporäre Lösung handelt, bis Hugo möglicherweise eine integrierte Funktion für das Abrufen des aktuellen OutputFormats bereitstellt. Am besten abonnierst Du das offene Issue auf GitHub, um über zukünftige Updates informiert zu bleiben.

[^1]: Ein Partial ist ein Hugo-spezifisches Template und wird im Projektverzeichnis unter `layouts/partials` abgelegt. Partials, welche keinen Inhalt ausgeben, sondern wie das vorliegende einen Wert zurück liefern, werden oftmals unter `layouts/partials/_functions` abgelegt. Dies ist aber keine Voraussetzung.

---
Foto von [Keith Misner](https://unsplash.com/photos/h0Vxgz5tyXA) auf [Unsplash](https://unsplash.com/).
