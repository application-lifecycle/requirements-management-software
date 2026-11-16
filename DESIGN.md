# Design: Requirements Management Software Directory

Locked Hallmark system for all pages in `docs/`.

## System
- Genre: modern-minimal
- Theme: Cobalt (`deal 1/3, seed requirements-management-software-open-e624·65d2590d·2026-11-16·r0`)
- Axes: light/grotesk-sans/cool · posture: restrained

## Tokens
`docs/styles/tokens.css` is the source of truth.
- Paper: `--color-paper`, `--color-paper-2`, `--color-paper-3`
- Ink & rules: `--color-ink`, `--color-ink-2`, `--color-muted`, `--color-rule`, `--color-rule-2`
- Graphite band: `--color-graphite`, `--color-graphite-2`, `--color-graphite-ink`, `--color-graphite-muted`
- Signals: `--color-accent` (electric cobalt), `--color-accent-2`, `--color-accent-wash`, `--color-accent-edge`
- Typography: `--font-display` ("Familjen Grotesk"), `--font-body` ("IBM Plex Sans"), `--font-outlier` ("JetBrains Mono" for code, CLI commands, and tabular IDs only).

## Controls
- Keycaps (`.key`, `.key--primary`) with 3px bottom edge, lifting 1px on hover and sinking on active.
- Cut-corner panels (`.cut`) with `--cut-l` bevels where supported, `--radius-card` fallback.
- Sentence-case, untracked labels and table headers in `--font-display` 500.

## Exports
`docs/styles/tokens.css`, `docs/styles/base.css`, `docs/styles/site.css`.
