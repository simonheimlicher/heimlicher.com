#!/usr/bin/env sh

# Build script for Vercel
# Based on https://www.brycewray.com/posts/2022/03/using-dart-sass-hugo-sequel/
# which is based on https://discourse.gohugo.io/t/using-dart-sass-hugo-and-netlify/37099/7

set -eu

DART_SASS_VERSION="${DART_SASS_VERSION:-1.85.1}"

BIN_DIR="${BIN_DIR:-$PWD/bin}"
FIRST_PATH_DIR=$(echo $PATH | cut -d':' -f1)
if [ -w "$FIRST_PATH_DIR" ]; then
  BIN_DIR=$FIRST_PATH_DIR
  echo "Using first directory in PATH as BIN_DIR=''$BIN_DIR"
else
  echo "First directory in PATH '$FIRST_PATH_DIR' is not writable. Using BIN_DIR='$BIN_DIR'"
  mkdir -p "$BIN_DIR"
fi


echo "Installing Dart Sass ${DART_SASS_VERSION} to BIN_DIR=${BIN_DIR}..."

# Download and extract Dart Sass directly into $BIN_DIR
curl -LJO "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"
tar -xf "dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz" -C "$BIN_DIR" --strip-components=1
rm -f "dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"

# Check if Dart Sass is found
echo "Checking Dart Sass version..."
sass --embedded --version

# Check if Hugo finds the Dart Sass executable
echo "Checking Hugo environment..."
hugo env

# Install Go to allow Hugo modules to be installed
echo "Installing Go..."
yum install -y golang

# Check if go is found
echo "Checking Go version..."
go version

# Install NPM modules
npm ci

# Install Hugo modules
echo "Installing Hugo modules..."
hugo mod get
