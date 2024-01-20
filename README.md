# [Professional website of Simon Heimlicher](https://simon.heimlicher.com/about/)

This repository hosts my professional website built with [Hugo](https://gohugo.io) based on my theme [Hugo Claris](https://github.com/simonheimlicher/hugo-claris).

## Continuous integration and deployment *(CI/CD)* with **GitHub Actions**

This repository contains a *GitHub Actions workflow* named **[Deploy Hugo site to Cloudflare Pages](https://github.com/simonheimlicher/heimlicher.com/actions/workflows/cloudflare-pages.yaml)** in the file `.github/workflows/cloudflare-pages.yaml`. This workflow is triggered on *push* to either the *main* or the *devel* branch.

### Deployment to *Cloudflare Pages*

The workflow builds the website and then deploys it to the **Cloudflare Pages** project corresponding to the branch.

| **Git branch** | **Cloudflare Pages project**  | **Cloudflare domain**                 | **Custom domain**                |
| -------------- | ----------------------------- | ------------------------------------- | -------------------------------- |
| **main**       | heimlicher                    | <https://heimlicher.pages.dev>        | <https://simon.heimlicher.com>   |
| **stage**      | heimlicher-stage              | <https://heimlicher-stage.pages.dev>  | <https://stage.heimlicher.com>   |

## How to get this website up and running

### Get everything required

1. [Install Hugo](https://gohugo.io/overview/installing/) and [Dart Sass](https://sass-lang.com/dart-sass/)
2. Clone this repository
3. Install the required Node packages

#### 1. Get **[Hugo]**(https://gohugo.io/overview/installing/) and **[Dart Sass](https://sass-lang.com/dart-sass/)**

Hugo is available in two editions: *standard* and *extended*. This website requires the **extended edition** version **0.121.0** or later.

The theme also requires **Dart Sass** in version **1.70.0** or later to compile the *SASS* files of the theme to *CSS*.

On a Mac with [homebrew](https://brew.sh/) already installed, you can simply run

```zsh
brew install hugo sass/sass/sass
```

This will install the *extended* edition of Hugo. There is no *standard edition* in Homebrew, which makes life simple.

#### 2. Clone this repo

```zsh
git clone https://github.com/simonheimlicher/heimlicher.com.git
cd heimlicher.com
```

#### 3. Install the required Node packages

```zsh
npm install
```

### Local development

For development, run

```zsh
hugo server
```

### Build for deployment

To build for deployment, run

```zsh
hugo
```

## Organization of this repository

The repository contains the following:

1. **Content:** articles with their associated images
2. **Assets:** assets such as share images
3. **Configuration:** configuration files for all environments (`devel`, `test`, `stage`, `prod`) of `heimlicher.com`.

### 1. Content

Under `/content/` this repository contains the source of all pages of this website in the form of Hugo *Page Bundles*, which comprise a Markdown file named `index.mx` and associated images.

### 2. Assets

The directory `/assets/` contains only the share images, which are included in the respective sections of the `<head>` node for [*LD+JSON*](https://schema.org), [*OpenGraph*](https://opengraph.org) and

### 3. Configuration

The configuration is primarily contained in the directory `config/_default`. The other directories (i.e., `devel`, `test`, `stage` and `prod`) contain only configuration that deviates from the `_default`.
