# InternHub

A full-stack Flask internship portal integrated with Supabase.

## Setup Instructions
1. Create a Supabase project and execute the SQL script in `database/database.sql`.
2. Copy `.env.example` to `.env` and fill in your Supabase credentials.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## Updating an existing PythonAnywhere deployment

The Supabase database is hosted separately. Do not rerun the schema script when
connecting to an existing database.

1. Open a console in the virtual environment configured on PythonAnywhere's Web
   tab. Change to the deployed repository folder and run:
   ```bash
   git pull --ff-only origin main
   python -m pip install -r requirements.txt
   python -m pip check
   ```
2. Create or update `.env` next to `app.py` on PythonAnywhere. This file is ignored
   by Git and must be configured separately on the host. Set `SUPABASE_URL` and
   `SUPABASE_KEY` to the existing project's URL and legacy JWT-style `anon` key.
   The pinned Supabase SDK does not accept `sb_publishable_...` keys. Set
   `SECRET_KEY` to a separate random Flask session secret, not a Supabase secret
   key, and set `FLASK_DEBUG=False`.
3. Ensure the existing PythonAnywhere WSGI configuration adds the deployed
   repository folder to `sys.path` and imports `app` as `application`:
   ```python
   from app import app as application
   ```
   Configuration loads `.env` relative to the source files, regardless of the
   worker's current directory. Existing environment variables take precedence.
   PythonAnywhere runs the WSGI application; no separate Gunicorn command is needed.
4. Click Reload on the Web tab. Dependency and environment changes do not take
   effect in existing workers until the app reloads.
5. Check the error/server logs if registration reports database unavailability.
   `Invalid API key` indicates an incompatible key format; an unexpected `proxy`
   argument indicates the dependency fix was not installed in the web app's
   environment. A missing-configuration warning indicates absent or placeholder
   environment values.

These setup fixes do not address database access policies or application
authorization. Review those separately before using real user data.
