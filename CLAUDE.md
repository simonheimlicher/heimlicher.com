# AI Agent Context Guide: heimlicher.com

## Critical Rules

- ⚠️ **NEVER write or edit prose without invoking a skill first** - Content is the primary output of this project. Invoke `prose:author-prose` BEFORE writing and the `prose:prose-auditor` agent AFTER. No exceptions.
- ⚠️ **NEVER use Claude as commit author** - All commits must use the repository owner's git identity (`Simon Heimlicher <simon.github@heimlicher.com>`), not Claude or any AI assistant. This applies to all commits, including initial commits, amendments, and rebases.
- ⚠️ **NEVER commit without invoking a skill first** - Use `spec-tree:commit-changes` for every commit. Never run bare `git commit`.
- ⚠️ **NEVER call `hugo` directly** - Always use pnpm scripts (`pnpm run dev`, `pnpm run build`, etc.). The scripts load required env vars via dotenvx and use the correct Hugo version via HVM.
- ⚠️ **NEVER use agents to create or modify files** - Agents must only be used for read-only research. All file creation, editing, and writing must happen in the main conversation context.
- ✅ **When uncertain, ASK. Never guess content intent, tone, or audience.**

## MANDATORY: Use Skills for ALL Work

**THIS IS NON-NEGOTIABLE.** Before performing ANY task, invoke the appropriate skill.

### Required Skills

| User asks to...                                       | Skill to Invoke               |
| ----------------------------------------------------- | ----------------------------- |
| Write or edit content pages, blog posts, or any prose | `prose:author-prose`          |
| Review or improve prose quality                       | `prose:prose-auditor` (agent) |
| Commit changes                                        | `spec-tree:commit-changes`    |

### Required Skills by Situation

| You're thinking...                             | Skill to invoke               | Why                                           |
| ---------------------------------------------- | ----------------------------- | --------------------------------------------- |
| "I need to draft or rewrite a content section" | `prose:author-prose`          | All prose must go through the authoring skill |
| "This draft is done, let me commit"            | `prose:prose-auditor` (agent) | Audit quality BEFORE committing               |
| "Time to commit"                               | `spec-tree:commit-changes`    | Follows Conventional Commits conventions      |

## Enforcement: STOP Triggers

If you find yourself doing any of these, **STOP immediately**:

- Writing or editing Markdown content without invoking `prose:author-prose` → STOP, invoke skill
- Considering prose "done" without the `prose:prose-auditor` agent → STOP, invoke it
- Running `git commit` without `spec-tree:commit-changes` → STOP, invoke skill
- Calling `hugo` directly instead of using pnpm scripts → STOP, use `pnpm run ...`
- Using an Agent to create, edit, or write ANY file → STOP, agents are read-only research tools

**Load the skill FIRST, then proceed.**

---

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
pnpm run dev

# Production build (uses published module versions from go.mod)
pnpm run build

# Production build with local modules (uses go.work)
pnpm run build:workspace
```

Output goes to `public/`.

### All Available Scripts

| Script               | Purpose                                                         |
| -------------------- | --------------------------------------------------------------- |
| `dev`                | Dev server (port 1313) with local modules via `go.work`         |
| `build`              | Production build using published module versions (go.mod)       |
| `build:workspace`    | Production build using local modules via `go.work`              |
| `clean`              | Remove `public/` and `resources/_gen/` directories              |
| `dev:kill`           | Gracefully kill dev server on port 1313 (SIGTERM, then SIGKILL) |
| `dev:restart`        | Kill dev server if running, then start fresh                    |
| `rebuild:workspace`  | Shortcut for `clean` + `build:workspace`                        |
| `mod-pack`           | Run `hugo mod npm pack` to regenerate `package.json`            |
| `mod-pack:workspace` | Run `hugo mod npm pack` with local modules via `go.work`        |

### Dependencies & Setup

- **Package Management**: this project uses **pnpm**, not npm. `packageManager` in
  `package.hugo.json` pins the version, and `pnpm-lock.yaml` is the committed lockfile.
  - Run `pnpm install --frozen-lockfile` (preferred) or `pnpm install` to install
    necessary Node.js dependencies.
  - This step is **mandatory** before starting the development server.

```bash
pnpm install --frozen-lockfile   # Install Node.js dependencies (required)
pnpm run mod-pack                # Regenerate package.json from package.hugo.json
```

`pnpm-workspace.yaml` carries three settings that the build depends on. pnpm 11 reads
them there, not from `.npmrc`:

| Setting               | Why                                                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scriptShell`         | pnpm's own shell emulator cannot run the bash arrays in `dev:kill`                                                                                |
| `verifyDepsBeforeRun` | `mod-pack` rewrites `package.json`, so the implicit pre-script install must stay off                                                              |
| `ignoreScripts`       | No dependency runs install or build scripts. Without it, pnpm 11's `strictDepBuilds` default fails any cold install over unreviewed build scripts |

### Deployment

**Two pipelines build this site. Both must be green before a merge.**

| Pipeline                        | Serves                     | Config                                     | Trigger              |
| ------------------------------- | -------------------------- | ------------------------------------------ | -------------------- |
| **Cloudflare Pages** (traffic)  | `simon.heimlicher.com`     | `.github/workflows/cloudflare-pages.yml`   | Push to any branch   |
| Vercel (parallel target)        | `heimlicher-com.vercel.app`| `vercel.json` -> `.vercel/build.sh`        | Push to any branch   |

Cloudflare Pages is what visitors hit. Verify a change there first. `curl -sI
https://simon.heimlicher.com` returns `server: cloudflare`, never a Vercel header.

#### Cloudflare Pages

The workflow is a thin caller; the real logic is the reusable workflow
`simonheimlicher/claris-gh-actions/.github/workflows/build-hugo.yml@main`. Two Pages projects
are deployed per run:

| Pages project       | URL                    | Variable                        |
| ------------------- | ---------------------- | ------------------------------- |
| `heimlicher`        | simon.heimlicher.com   | `CLOUDFLARE_PROJECT_NAME`       |
| `heimlicher-debug`  | debug.heimlicher.com   | `CLOUDFLARE_PROJECT_NAME_DEBUG` |

`HUGO_VERSION` is a **repository variable** here, not a Vercel setting. The reusable workflow
installs dependencies from whichever lockfile is present -- `pnpm-lock.yaml` via corepack,
otherwise `npm ci`. A missing lockfile skips the install and Hugo's esbuild then fails with an
opaque `Could not resolve "posthog-js"` rather than an install error.

`CLOUDFLARE_API_TOKEN` needs two permissions: account-scoped **Cloudflare Pages: Edit** for the
deploy, and zone-scoped **Cache Purge: Purge** for `purge-modified.py`.

#### Vercel

Project `simonheimlicher/heimlicher`, linked via `.vercel/project.json` (gitignored).
`vercel.json` overrides the build with `.vercel/build.sh`. `VERCEL_ENV=production` maps to
`--environment=prod`, `preview` to `stage`.

Vercel-only settings that the repository cannot express:

- **`ENABLE_EXPERIMENTAL_COREPACK=1`** is required, or Vercel picks a pnpm version from the
  project creation date, ignores `packageManager`, and fails on the settings-only
  `pnpm-workspace.yaml`. Currently scoped to the `build/tooling` branch only.
- **`HUGO_VERSION`** is a Vercel env var, separate from the Cloudflare repository variable of
  the same name. The two drift independently.
- **Node.js Version** must satisfy `engines.node` in `package.json`; pnpm 11 needs >= 22.13.

Preview deployments are `noindex, nofollow`: the theme defaults `robots.index`/`follow` to
`false` and only `config/production/hugo.yaml` turns indexing on. Vercel previews are also
behind SSO (`prod_deployment_urls_and_all_previews`) with no bypass secret, so preview URLs
return a Vercel login page rather than the site.

## Local Development with Modules

A single `go.work` file references local module checkouts:

```go
go 1.24

use /Users/shz/Code/hugo/modules/hugo-claris/hugo-claris
use /Users/shz/Code/hugo/modules/claris-resources
use /Users/shz/Code/hugo/modules/fontawesome
```

The `dev` and `build:workspace` pnpm scripts automatically set `HUGO_MODULE_WORKSPACE=go.work`.

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
3. Run `pnpm install` to update `node_modules`

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

`hugo mod get` and `hugo mod clean` have no pnpm script wrapper, so they are the only
sanctioned direct `hugo` calls. Everything that builds or serves the site goes through a script.

To update a Hugo module dependency:

```zsh
hugo mod get -u github.com/simonheimlicher/hugo-claris
```

To regenerate `package.json` against the local module checkouts, use the script rather than
calling `hugo` yourself:

```zsh
pnpm run mod-pack:workspace
```

To clear the module cache (useful when local changes aren't being picked up):

```zsh
hugo mod clean
```

Always use pnpm scripts (`pnpm run dev`, `pnpm run build`, etc.) — never call `hugo` directly. See Critical Rules above.

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

**Known defect — `config/_default/configTaxo.yaml` is inert.** Hugo maps each filename under
`config/_default/` to a config key, so that file's contents land under a meaningless
`configTaxo` key and nothing reads them. `hugo config` resolves `timeout` to the default
`300s` rather than the file's `30000`, and the `privacy` block is empty, so
`youtube.privacyEnhanced`, `twitter.enableDNT`, and the Instagram and Vimeo simple modes are
all off. Merge the contents into `hugo.yaml` — do not trust that file.

### Inspecting Build Output

After `pnpm run build:workspace`, inspect the generated HTML:

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
pnpm run build:workspace

# Analyze resources
pnpm dlx tsx ~/Code/hugo/modules/hugo-claris/hugo-claris/perf/analyze-resources.mts public
```
