## Architecture Overview

### High-Level
- **Django app** running on a Windows PC exposes a local web UI over LAN
- **SQLite** stores meals, preferences, snoozes, and weekly history
- **ReportLab** generates PDF; **pywin32** sends jobs to default printer on Windows
- **Task Scheduler** runs a management command weekly to auto-generate and print

### Components
- `meals` app: categories, meals, preferences (heart), snoozes, archive
- `planning` app: weekly plan generation, history, like/dislike feedback
- `printing` app: PDF rendering, printer integration, templates
- `web` app: views/templates, Bootstrap UI, admin customizations

### Web UI
- Server-side rendered pages (Django templates) for MVP
- Mobile-first layout via Bootstrap; works on phone/tablet
- CSRF-protected form posts; light HTMX/vanilla JS for interactions (optional)

### APIs (Optional later)
- Read-only JSON endpoints for plan preview/history
- POST endpoints for generating plan and toggling preferences

### Networking & Access
- Bind server to LAN IP; accessible at `http://<PC-IP>:8000/`
- No exposure to the internet; optional auth gate with simple PIN

### Scheduling & Automation
- Management command: `python manage.py weekly_print` performs:
  - Generate upcoming week plan
  - Persist to DB and PDF
  - Send to printer (Windows) or store PDF for manual print

### Packaging
- Python venv; `.env` for configuration
- Optional: Windows shortcut/batch to start server; Task Scheduler XML template

### Profiles & Config
- Dev (Mac):
  - `ENV=dev`, bind to `127.0.0.1`, `DEBUG=True`, `PRINTING_MODE=none`
  - PDFs saved to disk for preview; no OS printing invoked
- LAN/Windows:
  - `ENV=prod`, bind to LAN IP, `DEBUG=False`, `PRINTING_MODE=windows`
  - `ALLOWED_HOSTS` set; optional PIN gate
- Common:
  - `DATA_DIR=./var` for prints/logs; all paths via `pathlib`

### Adapters
- `PrinterAdapter` interface with implementations:
  - `PdfOnlyPrinter` (default in dev): generate and store PDFs, no print
  - `WindowsPrinter`: use `pywin32` (`win32print`) to send to default printer
  - Optional `SumatraPrinter` fallback via CLI
- `SchedulerAdapter` guidance: dev/manual vs Windows Task Scheduler

### Desktop Shell (Optional later)
- If a desktop app is desired, wrap the web UI:
  - `pywebview` (Python-native, lightweight) or Electron/Tauri
  - Shell launches the Django server on a local port and loads it
  - Shell is purely a wrapper; core logic stays in Python/Django
