---
title: "Sharing and inheritance of Hugo page resources"
supertitle: Hugo partial
date: 2024-01-27T22:02:07+01:00
lastmod: 2024-01-27T22:02:07+01:00
description: "A Hugo partial that vastly improves resource management in Hugo sites by avoiding duplicate images in your content based on Page Bundles and Headless Bundles"
featured: false
image:
  feature:
    src: "images/keith-misner-h0Vxgz5tyXA-unsplash"
    alt:
    title:
    credit: ""
  # excerpt:
  #   src: "images/hugo_theme_claris-thumbnail"
  #   alt:
  #   title:
  #   credit: ''
  # share:
  #   src: "images/hugo_theme_claris-share"
  #   alt:
  #   title:
  #   credit: ''
  # search:
  #   src: "images/hugo_theme_claris-share"
  #   alt:
  #   title:
  #   credit: ''
tags:
  - hugo partial
series:
  - hugo snippets
---

Hugo’s Page Bundle model keeps content and its resources together, but it doesn’t help when multiple pages need the same image. The standard approach — duplicating the file in each bundle — works until it doesn’t: one update missed, one path wrong, and things break quietly.

This partial retrieves resources from a page bundle but walks up the content hierarchy if the resource isn’t in the current page’s bundle, stopping at site assets if nothing is found closer. A single shared image in a section’s `images/` directory becomes accessible to every page in that section with the same call used to fetch a page-local resource.

## Illustrative example

Let's consider the following example of a directory structure:

```zsh
content:
  articles:
    _index.md
    my-article:
      index.md
      images:
        feature-image.jpg
    images:
      index.md
      share-image.jpg
assets:
  images:
    logo.png
```

If you now use this partial in the file `content/articles/my-article/index.md`, you can access the three images by their relative paths.

### Accessing a feature image

As the feature image is specific to the article, it exists in the page bundle of the article `my-article`. We can access it using the following code:

```go-template
{{ $featureImage := partial "claris/_functions/resources/get" (dict 
        "Page" .
        "resource" "images/feature-image"
) }}
```

### Accessing a share image by traversing the file hierarchy

Now the share image might also be specific to the article, but in my case, I use the same share image for all articles. The share image hence only exists in the branch bundle of the articles section `articles`.

{{< note >}}

**Ensure to turn `images` directory into a headless bundle**: Add a file named `index.md` with the following content into every `images` directory that is part of a branch bundle (see below for an explanation what a branch bundle is)

```yaml
---
headless: true
---
```

{{< /note >}}

If we have properly set up the `images` directory under `articles` as a headless bundle, we can access the share image `share-image.jpg` from the page bundle `my-article` using the following code:

```go-template
{{ $shareImage := partial "claris/_functions/resources/get" (dict 
        "Page" .
        "resource" "images/share-image"
) }}
```

Perhaps surprisingly, the call to the `resources` partial is almost the same, even though we will get an image from a headless bundle one level up.

### Accessing the logo image from the global `assets` folder

Finally, the site's logo image will be the same for all articles. Hence, it makes sense to either put it into a headless bundle at the top of the `content` directory, or into the `assets` directory.

To access the share image, we use the following invocation of the `resources` partial:

```go-template
{{ $logoImage := partial "claris/_functions/resources/get" (dict 
        "Page" .
        "resource" "images/logo"
) }}
```

Again, the call to the `resources` partial is almost the same, even though we will get an image from the global `assets` directory.

## Basic usage

This partial accepts a dictionary with two key-value pairs: `Page` refers to the current page, while `$resourcePath` is the path of the resource. The path is treated as the prefix of the resource to be found, unless it ends with a file extension.

```go-template
{{ $resourcePath := "images/feature-image" }}
{{ $resourceArgs := (dict
"Page" .
"resource" $resourcePath
) }}

{{- $image := partial "claris/_functions/resources/get" $resourceArgs }}
```

#### Page Bundles in Hugo

Hugo categorizes Page Bundles into Leaf Bundles and Branch Bundles. Leaf Bundles are directories containing an `index.md` file and can include a variety of content and attachments for single pages. Branch Bundles, represented by `_index.md`, need to be used for sections and typically only contain non-page resources (source: [Hugo Page Bundles](https://gohugo.io/content-management/page-bundles/)).

### Headless Bundles

For Branch Bundles, the partial employs a workaround using Headless Bundles. By adding `headless: true` to the front matter of an `index.md` file within a directory, the directory can host resources similarly to a Leaf Bundle (detailed at [Hugo Headless Bundles](https://gohugo.io/content-management/page-bundles/#headless-bundle)).

### Parameters and Return Values

The partial uses the current page and the resource path as parameters, returning a Hugo resource object or `false` if not found.

### Resource Handling

Preference is given to page resources, with a fallback to site resources if the desired resource isn't found in the current page or its ancestors (source: [Hugo Page Resources](https://gohugo.io/content-management/page-resources/)).

## Debugging Features

A `$debug` variable can be set to `true` for insights into the operational flow, aiding in troubleshooting and enhancements.

## How to Get This Partial

This partial is part of my Hugo module `claris-resources` and [hosted on GitHub](https://github.com/simonheimlicher/claris-resources). To use it in your Hugo website, add the following to your `config/_default/hugo.yaml` (or `hugo.toml`) file:

```yaml
module:
  imports:
    - path: github.com/simonheimlicher/claris-resources
```

This partial grew out of my own site's needs. {{< obfuscated-email "Let me know if you run into cases it doesn't handle" >}} — I'm happy to extend it.
