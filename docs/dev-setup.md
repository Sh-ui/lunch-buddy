## Dev Setup (Mac)

### Prereqs
- Python 3.11+

### Steps
1. Create venv and install dependencies:
   - `python3 -m venv .venv && source .venv/bin/activate && pip install -U pip && pip install -r requirements.txt`
2. Initialize database and run server:
   - `python manage.py migrate && python manage.py runserver 127.0.0.1:8000`

### Environment
- Defaults are dev-friendly; optional env vars:
  - `ENV=dev`
  - `PRINTING_MODE=none`
  - `DATA_DIR=./var`
  - `PORT=8000`

Open http://127.0.0.1:8000 to see the home page scaffold.


