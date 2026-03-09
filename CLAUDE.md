# AI Agent Context Guide: heimlicher.com

## Quick Start

1. Read this file for site overview
2. See `~/Code/hugo/modules/hugo-claris/hugo-claris/CLAUDE.md` for theme details

## Project Overview

This is a Hugo website using the "Hugo Claris" theme, integrated as a Go module. The project follows a trunk-based workflow on the `main` branch.

## Key Development Requirements

### Environment Variables

- **`HUGO_CLARIS_AUTHOR_EMAIL`**: This environment variable is **REQUIRED**. It must be set to the author's email address (e.g., in `.env`).

### Quick Start Commands

```bash
# Development server (port 1313, uses local modules via go.work)
npm run dev

# Production build (uses published module versions from go.mod)
npm run build

# Production build with local modules (uses go.work)
npm run build:workspace
```

Output goes to `public/`.

### All Available Scripts

| Script               | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| `dev`                | Dev server (port 1313) with local modules via `go.work`   |
| `build`              | Production build using published module versions (go.mod) |
| `build:workspace`    | Production build using local modules via `go.work`        |
| `clean`              | Remove `public/` and `resources/_gen/` directories        |
| `rebuild:workspace`  | Shortcut for `clean` + `build:workspace`                  |
| `mod-pack`           | Run `hugo mod npm pack` to regenerate `package.json`      |
| `mod-pack:workspace` | Run `hugo mod npm pack` with local modules via `go.work`  |

### Dependencies & Setup

- **NPM Package Management**:
  - Run `npm ci` (preferred) or `npm install` to install necessary Node.js dependencies.
  - This step is **mandatory** before starting the development server.

```bash
npm ci                    # Install Node.js dependencies (required)
npm run mod-pack          # Regenerate package.json from package.hugo.json
```

| Branch | Environment | Config            | Deployment URL       | Trigger             |
| ------ | ----------- | ----------------- | -------------------- | ------------------- |
| `main` | Production  | `config/_default` | simon.heimlicher.com | Push to origin/main |

## Local Development with Modules

A single `go.work` file references local module checkouts:

```go
go 1.24

use /Users/shz/Code/hugo/modules/hugo-claris/hugo-claris
use /Users/shz/Code/hugo/modules/claris-resources
use /Users/shz/Code/hugo/modules/fontawesome
```

The `dev` and `build:workspace` npm scripts automatically set `HUGO_MODULE_WORKSPACE=go.work`.

## Technical Stack

- **Static Site Generator**: Hugo
- **Theme**: Hugo Claris (Go Module)
- **Languages**: HTML, CSS, JavaScript, Go (templates)

---

## Hugo-Specific Knowledge

### NPM Dependencies with `hugo mod npm pack`

Hugo uses a **two-file system** for npm dependencies:

| File                | Purpose                                                                                  |
| :------------------ | :--------------------------------------------------------------------------------------- |
| `package.hugo.json` | **Source of truth** - Hugo reads dependencies from this file                             |
| `package.json`      | **Generated output** - Created by `hugo mod npm pack` from all `package.hugo.json` files |

**Critical**: To add or remove npm dependencies, edit `package.hugo.json`, NOT `package.json`. Running `hugo mod npm pack` regenerates `package.json` by merging:

1. The project's `package.hugo.json`
2. All `package.hugo.json` files from Hugo modules in the dependency tree

The `comments.dependencies` section in generated files shows which module contributed each dependency.

**Workflow to remove a dependency**:

1. Remove from `package.hugo.json` in BOTH the project AND any Hugo modules that declare it
2. Run `hugo mod npm pack` to regenerate `package.json`
3. Run `npm install` to update `node_modules`

### Hugo's Built-in esbuild

Hugo has **esbuild compiled into the binary** for `js.Build`. You do NOT need esbuild as an npm dependency. The npm esbuild package is unnecessary and can be safely removed.

### Image Processing Memory Limits (Hugo v0.153+)

Hugo's WASM-based WebP encoder has a **fixed memory ceiling** (~6 megapixels by default). This affects srcset generation:

- Images exceeding the MP limit cannot be encoded to WebP
- The limit is configurable via `site.Params.images.maxOutputMegapixels`
- The "include original" option was removed as it cannot be reliably fulfilled

**Srcset calculation uses a two-phase approach**:

1. **Phase 1**: Calculate IDEAL widths based on original image dimensions (ensures consistent steps like 384, 512, 768px)
2. **Phase 2**: Cap widths to the effective maximum (respecting MP limit) and deduplicate

This ensures intermediate widths remain consistent regardless of whether the original exceeds the limit, and the srcset always has a valid maximum entry.

### Module Updates

To update a Hugo module dependency:

```zsh
hugo mod get -u github.com/simonheimlicher/hugo-claris
```

To use local module development with workspace:

```zsh
HUGO_MODULE_WORKSPACE=go.work hugo mod npm pack
```

To clear the module cache (useful when local changes aren't being picked up):

```zsh
hugo mod clean
```

**CRITICAL**: Always use npm scripts (`npm run dev`, `npm run build`, etc.) - never call `hugo` directly. The scripts load required env vars via dotenvx and use the correct Hugo version via HVM.

---

## CSS/Font Performance Debugging

### Configuration Location

Style and font settings are in `config/_default/params.yaml`:

```yaml
assets:
  styles:
    split: true # true = critical + deferred bundles, false = single main bundle
    fonts:
      selfhosted: true
      family:
        sans: "Source Sans 3"
        serif: "Alegreya"
        mono: "DM Mono"
```

### Inspecting Build Output

After `npm run build:workspace`, inspect the generated HTML:

```bash
# Check CSS bundles
find public/styles -name "*.css" -exec sh -c \
  'echo "$1: $(wc -c < "$1") bytes"' _ {} \;

# Check inline critical CSS (split mode)
grep -o '<style[^>]*>' public/leadership/index.html

# Check deferred CSS loading
grep -o '<link[^>]*deferred[^>]*>' public/leadership/index.html

# Check font preload links
grep -o '<link[^>]*preload[^>]*font[^>]*>' public/leadership/index.html

# Check all link tags in head
grep -E '<link[^>]+>' public/leadership/index.html | head -20
```

### Analyzing Build Output

```bash
# Build with local modules
npm run build:workspace

# Analyze resources
npx tsx ~/Code/hugo/modules/hugo-claris/hugo-claris/perf/analyze-resources.mts public
```
