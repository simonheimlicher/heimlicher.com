---
title: Hugo function to obtain `OutputFormat` of current page context
date: 2023-03-17T07:42:36+01:00
lastmod: 2023-03-20T08:42:44.669Z
description: Hugo does not currently provide a function to obtain the current OutputFormat
  - this function provides the answer
featured: false
draft: false
# toc: true # Controls if a table of contents should be generated for first-level links automatically.
featureImage: images/keith-misner-h0Vxgz5tyXA-unsplash.jpg
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

Hugo does not currently provide a function to obtain the current OutputFormat — this partial provides a simple solution.

Hugo allows adding [custom output formats](https://gohugo.io/templates/output-formats/) — yet, up to and including version 0.111.0, it does not offer a function to provide the `OutputFormat` of the current page context. As Hugo provides two functions to list available `OutputFormat`s and those differ in whether they include the current `OutputFormat`, a simple call to [complement](https://gohugo.io/functions/complement/) provides the answer.

{{% note %}}
There is an [open issue on GitHub](https://github.com/gohugoio/hugo/issues/9368) regarding the lack of an `OutputFormat` property of the `Page` class. [Joe Mooring](https://github.com/jmooring) came up with the same solution as below. But he also adds an important caveat: the below only works as long as all declared `OutputFormat`s have the following declared in `config.toml`: 

```toml
notAlternative = false
```

{{% /note %}}

You can add the below snippet to `layouts/partials/_functions` to use it in your templates.

{{< responsive-code lang="go-html-template" title="output-format" >}}
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

---
Photo by [Keith Misner](https://unsplash.com/photos/h0Vxgz5tyXA) on [Unsplash](https://unsplash.com/).
