# Repository Guidelines

## Project Structure & Module Organization

PACEr is a German-language Flask web app. Main application code lives in `PACEr/`: `app.py` defines the Flask app factory and startup path, `models.py` contains SQLAlchemy models, and `helper.py` holds the core pace calculation logic. Route blueprints are in `PACEr/routes/`, reusable service code is in `PACEr/services/`, Jinja templates are in `PACEr/templates/`, and browser assets are in `PACEr/static/`. Tailwind source CSS is `PACEr/static/css/theme.css`; generated CSS should be written to `PACEr/static/build/theme.css`.

Root-level files include `requirements.txt` for Python dependencies, `tailwind.config.js` for Tailwind v3 configuration, and small JSON/Markdown project notes.

## Build, Test, and Development Commands

Create and activate a virtual environment before installing dependencies:

```powershell
python -m venv .PACEr
.PACEr\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the CSS watcher in one terminal:

```powershell
npx tailwindcss -i PACEr/static/css/theme.css -o PACEr/static/build/theme.css --watch
```

Start the Flask development server in another terminal:

```powershell
python .\PACEr\app.py
```

On first run, `PACEr/pacer.db` is created automatically and seeded with the default admin account. Delete the database only when intentionally resetting local state.

## Coding Style & Naming Conventions

Use Python `snake_case` for functions and variables, JavaScript `camelCase`, and descriptive route/service module names. Keep UI text and domain terminology in German to match the existing app. Follow the current Jinja style: templates extend `layout.html`, partials live under `PACEr/templates/partials/`, and route-specific pages stay in matching subdirectories. Prefer Tailwind utility classes and existing component classes from `theme.css` over one-off inline styles.

## Testing Guidelines

There is no committed automated test suite. For changes, manually verify the calculator flow, HTMX result updates, PDF export, feedback form, admin login, and tournament pages as relevant. If adding tests, place them under a new `tests/` directory and name files `test_*.py`; use `pytest` unless the project adopts a different framework.

## Commit & Pull Request Guidelines

Recent commits use short German summaries, often with a scope and colon, for example `UI-Overhaul: ...` or `Nachbesserungen: ...`. Keep commit subjects concise and outcome-focused.

Pull requests should include a brief change summary, manual verification steps, linked issue or context, and screenshots for visual changes. Mention any database reset, new environment variable, or dependency change explicitly.

## Security & Configuration Tips

Do not commit local databases, credentials, API keys, or generated secrets. CSRF, Flask-Login, and rate limiting are part of the app; preserve those protections when adding POST routes or admin functionality.
