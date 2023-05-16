# [Professional website of Simon Heimlicher](https://simon.heimlicher.com/about/)

This repository hosts my professional website built with [Hugo](https://gohugo.io/) and using my theme [Hugo Claris](https://github.com/hugo-claris/).

## How to set this up


### Get everything required

1. [Install Hugo](https://gohugo.io/overview/installing/)
2. Clone this repository
3. Install the dependencies for building the website

#### 1. Get [Hugo](https://gohugo.io/overview/installing/)

Hugo is available in two editions: *standard* and *extended*. The website requires the **extended edition**.

On a Mac with [homebrew](https://brew.sh/) already installed, you can simply run

```zsh
brew install hugo
```

This will install the *extended* edition. There is no *standard edition* in Homebrew, which makes life simple.

#### 2. Clone this repo

```zsh
git clone https://github.com/simonheimlicher/heimlicher.com.git
cd heimlicher.com
```

#### 3. Install dependencies

```zsh
npm install
```

#### 4. Run Hugo

For development, run

```zsh
hugo server
```

To build for deployment, run

```zsh
hugo
```

## Organization of this repository

The repository contains the following:

1. Content: 
2. Assets: 
3. Configuration: 

### 1. Content

Under `/content/` this repository contains the source of all pages of this website in the form of Markdown files.

### 2. Assets

### 3. Configuration
