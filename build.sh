#!/usr/bin/env sh

set -eu

DART_SASS_VERSION=1.69.5

npm ci

curl -LJO https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz
tar -xf dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz
cp -r dart-sass/* /usr/local/bin
rm -rf dart-sass*

yum install golang
hugo mod get
