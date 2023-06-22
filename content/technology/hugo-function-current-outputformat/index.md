---
categories:
- Hugo
date: "2023-03-17T07:42:36+01:00"
description: Hugo does not currently provide a function to obtain the current OutputFormat
  - this function provides the answer
draft: false
featured: false
image:
  feature: images/keith-misner-h0Vxgz5tyXA-unsplash.jpg
lastmod: "2023-03-20T08:42:44.669Z"
series:
- Hugo snippets
tags:
- Hugo partial
title: Hugo function to obtain `OutputFormat` of current page context
---

Hugo does not currently provide a function to obtain the current OutputFormat — this *partial[^1]* provides a simple solution.

Hugo allows adding [custom output formats](https://gohugo.io/templates/output-formats/) — yet, up to and including version 0.111.0, it does not offer a function to provide the `OutputFormat` of the current page context. As Hugo provides two functions to list available `OutputFormat`s and those differ in whether they include the current `OutputFormat`, a simple call to [complement](https://gohugo.io/functions/complement/) provides the answer.

{{% note %}}
There is an [open issue on GitHub](https://github.com/gohugoio/hugo/issues/9368) regarding the lack of an `OutputFormat` property of the `Page` class. [Joe Mooring](https://github.com/jmooring) came up with the same solution as below. But he also adds an important caveat: the below only works as long as all declared `OutputFormat`s have the following declared in `config.toml`: 

```toml
notAlternative = false
```

{{% /note %}}

You can add the below snippet to `layouts/partials/_functions` to use it in your templates.

{{< responsive-code lang="go-html-template" title="Save this as `layouts/partials/_functions/output-format`" >}}
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

In this post, we have seen how we can obtain the current OutputFormat with a simple partial in Hugo, even though Hugo itself does not yet offer a function for this purpose. It is important to note that this solution works under the condition that all declared OutputFormats have the parameter notAlternative = false declared in the config.toml file.

By adding the snippet mentioned above to layouts/partials/_functions, you can use the OutputFormat in your templates and dynamically adjust the output of the pages, depending on which format is currently being used.

Please remember that this is a temporary solution until Hugo possibly provides an integrated function for retrieving the current OutputFormat. It is best to subscribe to the open issue on GitHub to stay informed about future updates.

[^1]: A partial is a Hugo-specific template and is stored in the project directory under `layouts/partials`. Partials that do not output content but, like the present one, return a value, are often stored under `layouts/partials/_functions`. However, this is not a requirement.

---
Photo by [Keith Misner](https://unsplash.com/photos/h0Vxgz5tyXA) on [Unsplash](https://unsplash.com/).
