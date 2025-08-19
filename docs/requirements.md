## Product Requirements (MVP)

### Goals
- **Generate** a weekly lunch plan using weighted random selection
- **Manage** the meal pool (The Pantry): add, edit, remove, categorize
- **Prefer/Snooze** items: heart for boost; snooze until a date
- **Track** history of weekly plans and mark liked/disliked
- **Preview/Print** a PDF plan; auto-print on Windows
- **Accessible** from devices on the same home network

### Non-Goals (MVP)
- Multi-user accounts
- Cloud sync or remote access outside LAN
- Advanced analytics beyond like/dislike summaries

### User Stories
- As a user, I can add a meal with name and category so it can be selected
- As a user, I can heart a meal so it appears slightly more often
- As a user, I can snooze a meal until a date so it will not be selected
- As a user, I can generate a weekly plan and preview it before printing
- As a user, I can mark a week as liked/disliked after it prints
- As a user, I can re-generate the plan if I do not like the proposal (with safeguards)

### Constraints
- Local-first, single-machine server (Windows PC) on home LAN
- SQLite database; export/import to JSON for backup
- Deterministic seed option for reproducibility

### Success Metrics
- Time-to-first-plan under 2 minutes on fresh install
- No duplicate meal within 1 week window
- 100% successful PDF generation across supported OSes; Windows auto-print success rate > 95%

### Open Questions
- Exact categories (protein/veg/carb) and per-day composition
- How many meals per week; per-day constraints
- Weight tuning default values
