## Roadmap

Layered plan optimized for Mac-first development, cross-platform portability, and incremental testable slices.

### Phase 0 — Foundations (Mac-first)
 - [x] Repo setup, virtualenv, dependency pins
 - [x] Django project scaffold; apps: meals, planning, printing, web
 - [x] Bootstrap UI shell; Admin enabled
 - [x] Define adapter boundaries: `PrinterAdapter`, `SchedulerAdapter`, `PdfRenderer`
 - [x] Configuration via environment variables (`ENV`, `PRINTING_MODE`, `PORT`, `DATA_DIR`)
 - [x] Logging/layout under `var/` (prints, logs); paths via `pathlib`

### Phase 1 — Domain & Tests
 - [x] Models and migrations: `Category`, `Meal`, `MealSnooze`, `WeeklyPlan`, `PlanEntry`
 - [x] Selection service per spec with defaults (W, P, H)
 - [x] Unit tests for selection constraints (no duplicates, snooze respected, recency penalties)
 - [x] JSON import/export command and fixtures for quick bootstrapping

### Phase 2 — Pantry & Web UI
 - [x] Mobile-first SSR templates; Admin enabled for power editing
 - [x] Basic navigation and empty states
 - [x] CRUD UI for meals; heart/snooze/archive controls

### Phase 3 — Plan Generation & History
 - [ ] Generate weekly plan (per-day × categories)
 - [ ] History views and mark liked/disliked
 - [ ] Re-generate flow with safeguards

### Phase 4 — PDF Rendering (Dev-friendly)
 - [ ] ReportLab template; preview page
 - [ ] Store PDFs under `var/prints/YYYY/Week-YYYY-MM-DD.pdf`
 - [ ] No printing in dev (Mac): preview/download only

### Phase 5 — Printing Adapters (OS-specific)
 - [ ] `PdfOnlyPrinter` (default for Mac/dev)
 - [ ] `WindowsPrinter` via `pywin32` (`win32print`)
 - [ ] Optional fallback: `SumatraPDF -silent -print-to-default`
 - [ ] Robust error handling and logging

### Phase 6 — Automation & Ops
 - [ ] `weekly_print` management command (idempotent)
 - [ ] Scheduling adapter guidance
   - [ ] Windows Task Scheduler XML template
   - [ ] Dev: manual run or simple script
 - [ ] LAN access guide: `ALLOWED_HOSTS`, firewall rule, DHCP reservation, optional PIN gate

### Phase 7 — Packaging & Portability
 - [ ] Windows run profile using `waitress-serve`
 - [ ] Mac dev profile using Django dev server
 - [ ] Optional desktop shell (later): `pywebview` or Electron/Tauri wrapper that spawns the server and loads `http://localhost:<port>`
 - [ ] Backup/restore: JSON export/import UX

### Phase 8 — Enhancements
 - [ ] Analytics summary (simple stats, top liked)
 - [ ] Adjustable weights via settings UI
 - [ ] Optional REST API for mobile client

### Future Ideas
 - [ ] Cloud sync (Drive/Dropbox) or hosted backend
 - [ ] PWA with offline cache
 - [ ] Cross-platform desktop packaging for the shell if adopted
 - [ ] Ratings beyond like/dislike
