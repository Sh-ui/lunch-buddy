## Lunch Buddy

A local-first app that generates and prints a weekly lunch plan, accessible from any device on your home network. Manage your meal pool ("The Pantry"), set preferences (heart/snooze), track history, and print an auto-formatted weekly plan.

### Key Features
- **Weekly plan generation**: Weighted selection to avoid recent repeats and honor preferences
- **Pantry management**: Add/edit/remove meals and categories
- **Preferences**: Heart (boost), snooze (temporary exclude), archive (hide)
- **History & feedback**: Track past weeks and mark liked/disliked
- **Print & preview**: Generate a PDF and send to your Windows printer
- **Local web UI**: Use from phone/tablet via your home Wi‑Fi

### Tech Stack (Proposed)
- **Backend**: Python, Django, Django REST Framework
- **Frontend**: Django Templates + Bootstrap (MVP), optional SPA later
- **Storage**: SQLite (local), JSON import/export for backup
- **PDF**: ReportLab
- **Printing**: pywin32 (win32print) on Windows; download-only fallback on other OSes
- **Server**: Django dev server for development; Waitress for Windows production-like usage
- **Scheduling**: Windows Task Scheduler running a Django management command

### Quick Start (High Level)
1. Create a Python virtual environment
2. Install dependencies (to be added once code scaffolding is created)
3. Run database migrations
4. Start the Django server and open the local address on your phone
5. Use the Admin to seed categories/meals; generate a plan and print

Detailed steps will be added after initial scaffolding. Development will be Mac-first with printing disabled (PDF preview/download only) and Windows adapters enabled later. For now, see:
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/data-model.md`
- `docs/selection-algorithm.md`
- `docs/printing.md`
- `docs/roadmap.md`

### Naming
- App: Lunch Buddy
- Meal pool: The Pantry

### License
TBD (personal use by default).
