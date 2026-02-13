# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PACEr (**P**räzise **A**bstands-**C**alculierung für ein **E**rfolgreiches Ma**r**athon) is a German-language Flask web app that calculates split times for equestrian marathon events. It computes three time standards — Bestzeit (BZ), Erlaubte Zeit (EZ), Höchstzeit (HZ) — based on distance, speed, and race type (Wegstrecke, Hindernisstrecke, Schrittstrecke).

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run Tailwind CSS watcher (separate terminal)
npx tailwindcss -i PACEr/static/css/theme.css -o PACEr/static/build/theme.css --watch

# Start Flask dev server (runs on 0.0.0.0:5000)
python ./PACEr/app.py
```

On first start, the database (`PACEr/pacer.db`) is created automatically and a super-admin user is seeded (`admin` / `Potsdam1`). Delete `pacer.db` to reset.

## Architecture

**Flask app factory** (`create_app()`) in `PACEr/app.py`.

- **Database:** SQLite via Flask-SQLAlchemy, models in `PACEr/models.py`
- **Auth:** Flask-Login with `User` model, session-based, CSRF protection
- `PACEr/routes/` — Five blueprints:
  - `calculator.py` — Pace calculator (`/rechner`), HTMX API (`/api/calculate`), PDF export, OCR
  - `home.py` — Static pages (`/`, `/projectInfo`, `/aboutUs`, `/impressum`)
  - `report.py` — Bug reporting (`/reportProblem`)
  - `admin.py` — Admin panel (`/adminLogin`, `/adminTools`, `/viewReports`, `/changePassword`)
  - `tournament.py` — Tournament CRUD (admin) + public views (`/turniere`)
- `PACEr/helper.py` — Core business logic: `calculatePace`, `pace`, `oldPace`, `writeStatistics`
- `PACEr/services/` — Service modules:
  - `pdf_generator.py` — ReportLab PDF generation
  - `ocr_service.py` — Photo analysis (Anthropic API / Tesseract)
  - `csrf.py` — CSRF token generation + `@validate_csrf` decorator
  - `rate_limit.py` — In-memory login rate limiting (5 attempts / 5 min)
- `PACEr/models.py` — User, Report, UsageStatistic, Calculation, Tournament, AdminConfig
- `PACEr/templates/` — Jinja2 + HTMX, base template `layout.html`, partials in `partials/`
- `PACEr/static/css/theme.css` — Tailwind v3 source (built to `static/build/theme.css`)

## Auth System

- **Flask-Login** with `User` model (username, password_hash, role, last_login)
- `@admin_required` decorator on all admin routes (delegates to `@login_required`)
- `@validate_csrf` decorator on all POST routes — validates `_csrf_token` form field or `X-CSRFToken` header
- CSRF token available in templates via `{{ csrf_token() }}` (Jinja2 context processor)
- HTMX requests get CSRF header automatically via `htmx:configRequest` listener in `layout.html`
- Session config: 8h lifetime, HttpOnly, SameSite=Lax
- Login rate limiting: 5 failed attempts per IP → 5 min lockout
- Default super-admin: `admin` / `Potsdam1` (seeded on first start)

## Key Conventions

- UI text, variable names, and comments are in **German**
- Tailwind CSS: gray-900 bg, gray-800 header/footer, orange-600 accent, gray-400 text
- Component classes: `.card`, `.form-input`, `.btn-primary`, `.btn-secondary`, `.page-header`, `.section-header`
- Python: snake_case; JavaScript: camelCase
- Dependencies: Flask >=3.0, Flask-Login >=0.6, Flask-SQLAlchemy, ReportLab, Werkzeug >=3.0
- No test suite — verify manually after changes

## Gotchas

- Jinja2 has no `split` filter — pre-parse JSON in route, not template
- Tailwind v4 installed by default with `npm install -D tailwindcss` — use `tailwindcss@3` for config-based setup
- SQLite needs write permissions on both the `.db` file AND its parent directory (for journal files)
- When deleting `pacer.db` to reset, restart the server so `create_all()` + seed runs again
