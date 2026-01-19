#!/usr/bin/env bash

# Build script for Vercel - combines dependency installation AND build
# Based on https://gohugo.io/host-and-deploy/host-on-vercel/
#
# IMPORTANT: Go and other tools must be installed in the SAME script that runs
# hugo, because Vercel runs install and build commands in separate shells.
# The PATH modifications don't persist between phases.
#
# CACHING: Vercel caches node_modules/ between builds. We set Hugo's cacheDir
# to node_modules/.cache/hugo so processed images persist across builds.

set -euo pipefail

# Version defaults (can be overridden via environment variables)
DART_SASS_VERSION="${DART_SASS_VERSION:-1.97.2}"
GO_VERSION="${GO_VERSION:-1.25.5}"

# Hugo cache directory - Vercel caches node_modules/ between builds
# Export as HUGO_CACHEDIR so all hugo commands use it automatically
export HUGO_CACHEDIR="${PWD}/node_modules/.cache/hugo"

# Install all dependencies to ${HOME}/.local following Hugo's official approach
LOCAL_DIR="${HOME}/.local"

# =============================================================================
# FUNCTIONS
# =============================================================================

install_dart_sass() {
  echo "Installing Dart Sass ${DART_SASS_VERSION}..."
  mkdir -p "${LOCAL_DIR}"
  curl -sLJO "https://github.com/sass/dart-sass/releases/download/${DART_SASS_VERSION}/dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"
  tar -C "${LOCAL_DIR}" -xf "dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"
  rm -f "dart-sass-${DART_SASS_VERSION}-linux-x64.tar.gz"
  export PATH="${LOCAL_DIR}/dart-sass:${PATH}"

  echo "Verifying Dart Sass installation..."
  sass --embedded --version
}

install_go() {
  echo "Installing Go ${GO_VERSION}..."
  mkdir -p "${LOCAL_DIR}"
  curl -sL "https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz" | tar -C "${LOCAL_DIR}" -xzf -
  export PATH="${LOCAL_DIR}/go/bin:${PATH}"

  echo "Checking Go version..."
  go version
}

run_hugo_build() {
  local hugo_env="$1"
  echo "Building with environment: ${hugo_env}"
  hugo --gc --minify --environment="${hugo_env}"
}

# =============================================================================
# MAIN
# =============================================================================

# Install dependencies
install_dart_sass
install_go

# Verify Hugo environment
echo "Checking Hugo environment..."
hugo env

# Install NPM modules
echo "Installing Node modules..."
npm ci

# Install Hugo modules
echo "Installing Hugo modules..."
hugo mod get

# Ensure cache directory exists and report status
mkdir -p "${HUGO_CACHEDIR}"
CACHED_FILES=$(find "${HUGO_CACHEDIR}" -type f 2>/dev/null | wc -l | tr -d ' ')
if [ "${CACHED_FILES}" -gt 0 ]; then
  echo "Found ${CACHED_FILES} cached files in ${HUGO_CACHEDIR}"
else
  echo "No cached files found, starting fresh build."
fi

# Create hugo_stats.json if missing (required for CSS purging)
if ! [ -f hugo_stats.json ]; then
  echo "Running hugo to create 'hugo_stats.json' as this required file is missing."
  hugo --gc --minify

  if ! [ -f hugo_stats.json ]; then
    echo "Fatal error: Hugo failed to create hugo_stats.json"
    exit 1
  fi
fi

# Determine environment
ENVIRONMENT="${VERCEL_ENV:-production}"
if [ "$ENVIRONMENT" = "production" ]; then
  HUGO_ENV="prod"
elif [ "$ENVIRONMENT" = "preview" ]; then
  HUGO_ENV="stage"
else
  HUGO_ENV="devel"
fi

# Run the actual build
echo "Running production build..."
run_hugo_build "${HUGO_ENV}"

# Report cache status after build
CACHED_FILES=$(find "${HUGO_CACHEDIR}" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "Build complete! Cache now contains ${CACHED_FILES} files."
