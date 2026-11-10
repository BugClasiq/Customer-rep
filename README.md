# Customer-rep

GBOLAGADE's MiniMart — a support assistant web app: Flask API backend, static HTML/CSS/JS frontend, MySQL database, and a Groq-powered AI assistant (text + voice) served via Gradio.

The app runs fine **without Docker** — Flask serves the frontend itself. Docker files (`Dockerfile`s + `docker-compose.yml`) are included for anyone who does have Docker.

## Stack

| Layer    | Tech                                                        |
|----------|-------------------------------------------------------------|
| Frontend | Static HTML/CSS/JS (served by Flask locally, or by nginx in Docker) |
| Backend  | Flask (gunicorn in Docker), SQLAlchemy + Alembic migrations |
| AI       | Gradio UI (`ai/main.py`) + `POST /api/chat`, Groq LLM       |
| Database | MySQL 8 (or SQLite via `DATABASE_URL` for local runs)       |

## Quick start (no Docker)

Requires Python 3.12. Either a MySQL server with a database you control, or nothing at all if you use SQLite:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # Windows   (or: source .venv/bin/activate)
pip install -r requirements.txt
set DATABASE_URL=sqlite:///dev.db        # Windows; use export/DATABASE_URL on Linux/macOS
set GROQ_API_KEY=gsk_...                  # needed for the AI chat only
python run.py
```

Open http://127.0.0.1:5000 — Flask serves the landing page, login, signup and the support chat. (With MySQL instead of SQLite, unset `DATABASE_URL` and set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.)

Seed the demo data (an admin, a customer `john@gmail.com` / `customer123`, products, an order, knowledge-base entries) — **this drops and recreates all tables**:

```bash
python scripts/seed.py
```

Without `GROQ_API_KEY` everything works except the AI chat, which returns HTTP 503 / an error bubble.

## Quick start (Docker, if you have it)

```bash
git clone https://github.com/BugClasiq/Customer-rep.git
cd Customer-rep
cp .env.example .env       # then edit .env — at minimum set DB/SECRET values
docker compose up --build
```

First boot runs Alembic migrations automatically (`flask db upgrade`).

Seed the demo data (an admin, a customer, products, an order, knowledge-base entries) — **this drops and recreates all tables**:

```bash
docker compose exec backend python scripts/seed.py
```

Then open:

- Frontend: http://localhost:8080  (login: `john@gmail.com` / `customer123` after seeding)
- Backend API: http://localhost:5000/api/health
- Gradio AI assistant (full support chat): http://localhost:7860

### Services

| Service  | Port | Purpose                                     |
|----------|------|---------------------------------------------|
| frontend | 8080 | nginx serving the static site, `/api` proxy |
| backend  | 5000 | Flask API (`/api/login`, `/api/signup`, `/api/chat`, `/api/health`) |
| ai       | 7860 | Gradio Support AI assistant                  |
| db       | —    | MySQL 8 (volume `db_data`)                  |

`docker compose down -v` removes the database volume too.

## Environment variables

See `.env.example`. `GROQ_API_KEY` is required for the AI assistant to answer (`/api/chat` and the Gradio UI) — without it, chat returns HTTP 503 / an error bubble; everything else works. Set `GROQ_MODEL` to override the default `groq/compound-mini`.

For local (non-Docker) runs, `DATABASE_URL` overrides the MySQL connection string, e.g. `DATABASE_URL=sqlite:///dev.db python run.py`. Create the schema with `cd backend && set FLASK_APP=run.py && flask db upgrade` (works for SQLite too), or just run `python scripts/seed.py` to drop/recreate everything and load the demo data. The Gradio assistant is optional and only for the dedicated voice chat UI — run it with `python ai/main.py` on http://127.0.0.1:7860.

## Voice features (optional)

The Gradio assistant supports mic input / spoken replies, but those native dependencies are **not** installed by default:

```bash
pip install -r backend/requirements-voice.txt
```

They need a C toolchain and platform audio libraries (e.g. `portaudio19-dev`). Without them, text chat in the Gradio UI and `/api/chat` work normally; voice buttons degrade gracefully.

## Project layout

```
frontend/    Static site (login/signup/landing/chat) + nginx config + Dockerfile
backend/
  app/       Flask app factory, extensions, models, routes (auth, chat, health)
  ai/        Intent detection, Groq provider, response engine, speech, Gradio UI
  migrations/ Alembic migrations
  scripts/   seed.py (demo data), test.py (interactive order-CLI)
  run.py     Dev entrypoint (gunicorn is used in Docker)
docker-compose.yml
```

## Known limitations / notes

- Passwords: bcrypt, ≥8 chars enforced on signup. Emails are stored lowercase.
- `/api/chat` creates a new Groq API call per message; there is no rate limiting.
- The chat page requires `GROQ_API_KEY` and the seeded knowledge base to give useful answers.
- JWTs are wired (`flask-jwt-extended`) but nothing issues tokens yet — auth responses are plain JSON for now.
- `scripts/seed.py` is destructive (drops all tables). Don't run it against a database you care about.
