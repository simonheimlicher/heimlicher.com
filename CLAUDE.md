# AI Agent Context Guide: heimlicher.com

## Quick Start

1. Read this file for site overview
2. See `~/Sites/hugo/CLAUDE.md` for workspace-level context
3. See `~/Sites/hugo/modules/hugo-claris/root/CLAUDE.md` for theme details

## Project Overview

This is a Hugo website using the "Hugo Claris" theme, integrated as a Go module.

## Worktree Structure

This site uses git worktrees:

| Directory | Branch | Port | Purpose                           |
| --------- | ------ | ---- | --------------------------------- |
| `root/`   | devel  | 1315 | Active development (YOU ARE HERE) |
| `main/`   | main   | 1313 | Read-only reference to production |
| `stage/`  | stage  | 1314 | Read-only reference to staging    |

**Always work in `root/`** - the `main/` and `stage/` directories are for comparison only.

## Key Development Requirements

### Environment Variables

- **`HUGO_CLARIS_AUTHOR_EMAIL`**: This environment variable is **REQUIRED**. It must be set to the author's email address (e.g., in `.env`).

### Quick Start Commands

```bash
cd ~/Sites/hugo/sites/heimlicher.com/root

# Development server
npm run devel     # port 1313, uses go.mod versions
npm run stage     # port 1314
npm run prod      # port 1315

# Production build (uses go.mod versions)
npm run build

# Production build with local module worktrees
npm run build:workspace           # uses go.main.work (prod env)
npm run build:workspace:stage     # uses go.stage.work
npm run build:workspace:devel     # uses go.devel.work
```

Output goes to `public/`.

### All Available Scripts

| Script                  | Purpose                                                         |
| ----------------------- | --------------------------------------------------------------- |
| `devel`                 | Dev server (port 1313) with devel environment                   |
| `stage`                 | Dev server (port 1314) with stage environment                   |
| `prod`                  | Dev server (port 1315) with prod environment                    |
| `build`                 | Production build using published module versions (go.mod)       |
| `build:workspace`       | Production build using `go.main.work` (local modules, prod env) |
| `build:workspace:stage` | Build using `go.stage.work` (local modules, stage env)          |
| `build:workspace:devel` | Build using `go.devel.work` (local modules, devel env)          |
| `clean`                 | Remove `public/` and `resources/_gen/` directories              |
| `rebuild:workspace`     | Shortcut for `clean` + `build:workspace`                        |

### Dependencies & Setup

- **NPM Package Management**:
  - Run `npm ci` (preferred) or `npm install` to install necessary Node.js dependencies.
  - This step is **mandatory** before starting the development server.

```bash
npm ci                    # Install Node.js dependencies (required)
hugo mod npm pack         # Regenerate package.json from package.hugo.json
```

| Branch  | Environment | Config         | Deployment URL       | Trigger              |
| ------- | ----------- | -------------- | -------------------- | -------------------- |
| `main`  | Production  | `config/prod`  | simon.heimlicher.com | Push to origin/main  |
| `stage` | Staging     | `config/stage` | stage.heimlicher.com | Push to origin/stage |
| `devel` | Development | `config/devel` | localhost:1315       | Local only           |

## Local Development with Modules

Multiple `go.*.work` files reference local module checkouts at different branches:

| File            | Module Worktree             | Use Case                          |
| --------------- | --------------------------- | --------------------------------- |
| `go.main.work`  | `modules/hugo-claris/main`  | Test with production module code  |
| `go.stage.work` | `modules/hugo-claris/stage` | Test with staging module code     |
| `go.devel.work` | `modules/hugo-claris/root`  | Develop with local module changes |

Example (`go.devel.work`):

```go
go 1.21
use ../../../modules/hugo-claris/root    // devel branch of theme
use ../../../modules/claris-resources
use ../../../modules/fontawesome
```

The npm scripts automatically set `HUGO_MODULE_WORKSPACE` to the appropriate file.

## Deployment Notes

- **Staging**: Any push to the `stage` remote branch (`origin/stage`) automatically triggers a deployment to Cloudflare Pages at [stage.heimlicher.com](https://stage.heimlicher.com).

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

**CRITICAL**: Always use npm scripts (`npm run devel`, `npm run build`, etc.) - never call `hugo` directly. The scripts load required env vars via dotenvx and use the correct Hugo version via HVM.

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

### Comparing Stage vs Devel

```bash
cd ~/Sites/hugo/sites/heimlicher.com/root

# Build with devel module worktrees
npm run build:workspace:devel

# Analyze resources
npx tsx ../../../modules/hugo-claris/root/perf/analyze-resources.mts public --label devel

# Compare with stage
npm run build:workspace:stage
npx tsx ../../../modules/hugo-claris/root/perf/analyze-resources.mts public --label stage
```
