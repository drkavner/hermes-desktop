# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm run dev                # start Electron app in dev mode (electron-vite)
npm run build              # typecheck + build (typecheck must pass first)
npm run build:mac | :win | :linux   # platform packaging via electron-builder
npm run lint               # eslint --cache
npm run typecheck          # node + web tsconfigs (composite disabled)
npm run typecheck:node     # main + preload only
npm run typecheck:web      # renderer only
npm test                   # vitest run (single pass)
npm run test:watch         # vitest watch mode
npx vitest run path/to/file.test.ts                # single file
npx vitest run -t "test name substring"            # single test by name
```

Vitest config (`vitest.config.ts`) uses `jsdom` and globs `src/**/*.test.{ts,tsx}` and `tests/**/*.test.ts`. Path aliases `@renderer` and `@shared` resolve to `src/renderer/src` and `src/shared`.

## Architecture

This is a white-labeled Electron desktop wrapper around the upstream **`hermes-agent` Python CLI**. The app does not implement agent logic itself — it installs, configures, and talks to the CLI installed at `~/.hermes/`. The user-facing brand is "Cerebratech AI"; internal identifiers (paths, IPC channels, API surface) keep the `hermes` prefix because they reference the actual upstream tool. Do not rename these without coordinating across both processes and the test suite.

**Three Electron processes, three source roots:**

- `src/main/` — Node-side, has filesystem and child-process access. Owns all integration with the `hermes` CLI, SQLite, and installer scripts.
- `src/preload/` — context bridge. `index.ts` defines `hermesAPI` and exposes it on `window.hermesAPI`; `index.d.ts` declares the matching `HermesAPI` interface. The preload surface is asserted by `tests/preload-api-surface.test.ts` (regex-parses both files and compares method names) — keep `index.ts` and `index.d.ts` in lockstep or that test fails.
- `src/renderer/src/` — React 19 + Tailwind 4 UI. Talks to main only via `window.hermesAPI`. Screens live in `screens/<Name>/`; shared bits in `components/`.

**Key main-process modules:**

- `installer.ts` — exports the canonical path constants (`HERMES_HOME`, `HERMES_REPO`, `HERMES_PYTHON`, `HERMES_SCRIPT`, `HERMES_ENV_FILE`, `HERMES_CONFIG_FILE`) and `getEnhancedPath()` for spawning the CLI with the user's shell PATH (Electron launched from Finder/GUI doesn't inherit terminal env). Also handles first-run install via the upstream curl script, doctor, and update flows.
- `hermes.ts` — chat orchestration. Local mode spawns the `hermes` CLI; remote mode hits a `Cerebratech AI API server` over HTTP at the configured URL. SSE is parsed with `sse-parser.ts`. The constant `LOCAL_API_URL = http://127.0.0.1:8642` is the upstream server's default port.
- `sse-parser.ts` — pure SSE parsing extracted so it's testable without Electron/HTTP. Handles the upstream `hermes.tool.progress` custom event (do not rename — it's the wire format).
- `config.ts`, `profiles.ts` — read/write `~/.hermes/.env`, `~/.hermes/config.yaml`, and per-profile dirs.
- `sessions.ts` — read-only SQLite (`better-sqlite3`) on `~/.hermes/state.db` with FTS5 for session search. `better-sqlite3` is marked `external` in `electron.vite.config.ts` and rebuilt natively by `electron-builder install-app-deps` (the `postinstall` script).
- `index.ts` — registers all `ipcMain.handle(...)` channels, builds the app menu, configures auto-updater (electron-updater via `dev-app-update.yml` and `electron-builder.yml` `publish`).

**IPC contract:** Every renderer call goes through `window.hermesAPI.<method>` → preload `ipcRenderer.invoke("channel-name")` → main `ipcMain.handle("channel-name", ...)`. When adding a method, update all three: `src/preload/index.ts`, `src/preload/index.d.ts`, `src/main/index.ts`. `tests/ipc-handlers.test.ts` and `tests/preload-api-surface.test.ts` enforce the surface.

**Internationalization:** `src/shared/i18n/` is plain TS modules (no i18next runtime in shared). Locales live in `locales/en/` and `locales/zh-CN/`, one file per feature area. `src/renderer/src/components/I18nProvider.tsx` exposes `useI18n()` to React. The shared `t()` function falls back to English, then to the key itself. Keep en and zh-CN keys in sync — adding a key in en without zh-CN is allowed (falls back), but renaming requires both.

**Remote mode:** When `getConnectionConfig().mode === "remote"`, `src/main/hermes.ts` skips spawning the local CLI and proxies HTTP to the configured server. The renderer shows `RemoteNotice` for screens whose data lives on the server (memory, profiles, etc.) — wrap such screens accordingly.

## White-label notes

User-visible "Cerebratech AI" strings are in i18n locale files, the main-process dialog/menu titles, `electron-builder.yml` (`productName`, `appId: ai.cerebratech.desktop`), `package.json`, and the splash/logo `alt` text. Internal identifiers (`HERMES_*` paths, `hermesAPI`, IPC channel names, `hermes.tool.progress` event, install script URL pointing at `NousResearch/hermes-agent`) intentionally retain the `hermes` name because they bind to the underlying CLI.

## Testing notes

- `tests/constants.test.ts` currently has 2 pre-existing failures related to i18n keys vs. resolved labels (e.g. asserts `label: "Auto-detect"` but receives `"constants.autoDetect"`). These are unrelated to most changes — verify any new failure isn't masked by them.
- `tests/preload-api-surface.test.ts` parses `src/preload/index.ts` and `index.d.ts` with regex; if you reformat those files in a way that breaks the `interface HermesAPI { ... }` block or the `hermesAPI = { ... }` object literal layout, this test will fail.
