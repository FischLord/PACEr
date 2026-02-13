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
  - `home.py` — Landing page (`/`), Projekt-Info (`/projektInfo`), About (`/aboutUs`), Impressum (`/impressum`)
  - `report.py` — Feedback form (`/reportProblem`)
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
- `PACEr/static/js/` — `layout.js` (mobile menu, stagger animations), `calculator.js` (validation, mode toggle), `notification.js` (toasts), `reportProblem.js`

## Design System

**Theme:** Dark, sporty (Strava/Nike-Run-Club-inspired). Inter font via Google Fonts.

### Color Tokens (defined in `tailwind.config.js`)
- **Surface:** `surface` (#0a0a0f), `surface-raised` (#141419), `surface-overlay` (#1c1c24), `surface-border` (#2a2a35)
- **Accent:** `accent` (#f97316 orange), `accent-hover` (#fb923c)
- **Time colors:** `time-bz` (#4ade80 green), `time-ez` (#f97316 orange), `time-hz` (#f87171 red)
- **Text:** `text-primary` (#f5f5f5), `text-secondary` (#a1a1aa), `text-muted` (#71717a)

### Component Classes (defined in `theme.css`)
- **Surfaces:** `.card`, `.card-hover` (lift + accent glow), `.glass` (backdrop-blur)
- **Forms:** `.form-input`, `.form-select`, `.form-label` (uppercase, tracking-wide)
- **Buttons:** `.btn-primary` (accent, shadow-glow), `.btn-secondary`, `.btn-icon`, `.btn-danger`
- **Typography:** `.page-title` (text-4xl md:5xl, extrabold), `.section-header` (text-2xl, bold)
- **Chips:** `.chip` with `.peer:checked ~ .chip` auto-activation (no JS needed)
- **Slider:** `.range-slider` (w-6 h-6 thumb, accent shadow)
- **Timer:** `.time-display`, `.time-bz`, `.time-ez`, `.time-hz`
- **Flip Cards:** `.flip-card`, `.flip-card-inner`, `.flip-card-front`, `.flip-card-back` (CSS 3D flip), `.flip-card-backdrop` (mobile overlay). Mobile uses JS FLIP animation (position capture → fixed → animate expand/collapse) with `transitionend` + `setTimeout` fallback for cleanup
- **Timeline:** `.timeline-line` (vertical 2px line), `.timeline-dot` (12px accent circle)
- **Decorative:** `.accent-bar`, `.clip-angle`, `.loading-skeleton`, `.stagger-item`
- **Nav:** `.nav-link`, `.nav-link-active`

### Tailwind Safelist
`grid-cols-2`, `grid-cols-3`, `grid-cols-4` are safelisted for dynamic Jinja classes.

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
- "Probleme melden" renamed to **"Feedback"** in nav/footer, "Über uns" renamed to **"Über mich"**
- Python: snake_case; JavaScript: camelCase
- Dependencies: Flask >=3.0, Flask-Login >=0.6, Flask-SQLAlchemy, ReportLab, Werkzeug >=3.0
- No test suite — verify manually after changes

## Template Structure

- `layout.html` — Base: glass navbar (logo + Inter font), slide-in mobile overlay, footer with accent-bar, HTMX lifecycle (opacity transitions)
- `projektInfo.html` — Landing page (hero, features, how-it-works, flip-card sport showcase, CTA). Also serves as `/`. Flip cards use FLIP animation on mobile (expand to overlay with backdrop, animate back on close)
- `calculator/rechner.html` — Two-column: form (2/3) + info sidebar with BZ/EZ/HZ cards, steps, tournament hint (1/3). Sidebar hidden in result view. Segmented control toggle (Auto/Manuell), loading skeleton
- `partials/form_new.html` — Auto mode: chips for Streckenart, range slider for Tempo (slider + ticks + labels share one `flex-1` container for alignment)
- `partials/form_old.html` — Manual mode: timer-style Min:Sek inputs
- `partials/results.html` — Meta card with large numbers, color-coded timer table, PDF/new-calc actions
- `tournaments/index.html` — Card grid with hover-lift, date badges, subtitle when tournaments exist
- `tournaments/detail.html` — Accordion with BZ/EZ/HZ pill badges
- `admin/` — 5 templates extending `adminTools.html` sidebar layout
- `reportProblem.html` — Two-column: FAQ accordion (2/5) + feedback form (3/5). FAQ has 3 entries (Rundung, BZ/EZ-Abstand, LPO-Erlaubnis) + contact card
- `aboutUs.html` — Full-width sections: hero banner with gradient + profile image, 3 facts cards grid, wider "Über mich" card (max-w-3xl), vertical timeline (5 milestones), 3-col gallery placeholders, CTA + contact
- `impressum.html` — Contact cards grid at top, `<details>` accordions for each legal section (Inhalte open by default)

## Gotchas

- Jinja2 has no `split` filter — pre-parse JSON in route, not template
- Tailwind v4 installed by default with `npm install -D tailwindcss` — use `tailwindcss@3` for config-based setup
- SQLite needs write permissions on both the `.db` file AND its parent directory (for journal files)
- When deleting `pacer.db` to reset, restart the server so `create_all()` + seed runs again
- `peer-checked:` variant cannot apply to custom `@apply`-based component classes — use CSS selector `.peer:checked ~ .chip` instead
- AdminConfig model exists in `models.py` but is unused (legacy from pre-auth migration)
- Flip card mobile overlay: `transitionend` is unreliable for cleanup — always pair with a `setTimeout` fallback to remove inline styles, placeholder, and backdrop
- Slider tick alignment: ticks container must share the exact same parent as the `<input type="range">` (same `flex-1` wrapper) — separate flex rows cause progressive misalignment
