#!/usr/bin/env bash

# Build script for Vercel - combines dependency installation AND build
# Based on https://gohugo.io/host-and-deploy/host-on-vercel/
#
# IMPORTANT: Go and other tools must be installed in the SAME script that runs
# hugo, because Vercel runs install and build commands in separate shells.
# The PATH modifications don't persist between phases.
#
# CACHING: Vercel caches node_modules/ between builds. We leverage this by
# storing Hugo's generated resources (processed images, CSS) in node_modules/.cache
# to dramatically reduce build times for unchanged assets.

set -euo pipefail

# Version defaults (can be overridden via environment variables)
DART_SASS_VERSION="${DART_SASS_VERSION:-1.97.1}"
GO_VERSION="${GO_VERSION:-1.25.5}"

# Caching directories - Vercel caches node_modules/ between builds
CACHE_DIR="./node_modules/.cache/hugo-resources"
GEN_DIR="./resources/_gen"

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

restore_cache() {
  if [ -d "${CACHE_DIR}" ]; then
    echo "Restoring cached resources from ${CACHE_DIR}..."
    rm -rf "${GEN_DIR}"
    mkdir -p "${GEN_DIR}"
    cp -a "${CACHE_DIR}/." "${GEN_DIR}/"
    echo "Restored $(find "${GEN_DIR}" -type f | wc -l) cached files."
  else
    echo "No cached resources found at ${CACHE_DIR}, starting fresh."
  fi
}

save_cache() {
  if [ -d "${GEN_DIR}" ]; then
    echo "Saving generated resources to cache..."
    rm -rf "${CACHE_DIR}"
    mkdir -p "${CACHE_DIR}"
    cp -a "${GEN_DIR}/." "${CACHE_DIR}/"
    echo "Cached $(find "${CACHE_DIR}" -type f | wc -l) files to ${CACHE_DIR}."
  else
    echo "No generated resources found at ${GEN_DIR}, skipping cache."
  fi
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

# Restore cached resources BEFORE building
restore_cache

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

# Save generated resources to cache AFTER building
save_cache

echo "Build complete!"
