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

## Deploy everything on Railway (one place)

Everything runs as **one web service** (Flask serves the frontend, `/api/*` and the chat) plus **one MySQL plugin** in the same project. The optional Gradio UI can be a second service.

1. Push this repo to GitHub (already done).
2. At railway.app: **New Project → Deploy from GitHub repo** → pick `BugClasiq/Customer-rep`.
3. **+ New → Database → MySQL**.
4. On the web service's **Variables** tab:
   - `DATABASE_URL` — reference the plugin (e.g. `${{MySQL.MYSQL_URL}}`); cloud plugins hand out `mysql://...`, and this app rewrites it to `mysql+pymysql://...` automatically.
   - `SECRET_KEY`, `JWT_SECRET_KEY` — any long random strings.
   - `GROQ_API_KEY` — required for the AI chat (`/api/chat`).
5. On the web service's **Settings** tab: **Root Directory** = `backend`. Railway detects `backend/Dockerfile`, applies migrations on boot (`flask db upgrade`), and serves on `$PORT`.
6. **Networking → Generate Domain** → open it. You should land on the MiniMart landing page; `/<domain>/api/health` returns `{"status":"ok"}`.
7. Demo data: open a **Shell** on the service and run `python scripts/seed.py` (drops and recreates all tables). Log in as `john@gmail.com` / `customer123`.
8. Optional Gradio UI: **+ New → GitHub repo** (same repo) → **Root Directory** `backend`, **Custom Start Command** `python ai/main.py`, variable `GRADIO_SERVER_NAME=0.0.0.0`. It binds Railway's `$PORT` automatically. Text chat works; mic input additionally requires `pip install -r requirements-voice.txt`, which needs native audio libraries.

Note: Railway is not free — you get trial credit and the MySQL plugin consumes credits (usage-based, a few dollars/month).

## Deploy everything on Render (free)

One Render web service (free tier) serves the frontend, `/api/*` and the chat. MySQL comes from [Aiven's](https://aiven.io/free-mysql) free tier (Render has no free MySQL); the code rewrites its `mysql://` URL for you.

**A. Get a free MySQL (5 minutes)**
1. Sign up at aiven.io → **New project? → Free MySQL** → create the free plan.
2. Once running, copy the **Connection URI** (`mysql://user:password@host:port/defaultdb`).

**B. Deploy the app**
1. render.com → **New → Blueprint** → connect your GitHub repo → select `BugClasiq/Customer-rep`.
2. Render reads `render.yaml` and asks for `DATABASE_URL` (paste the Aiven URI) and `GROQ_API_KEY` (from console.groq.com). `SECRET_KEY`/`JWT_SECRET_KEY` are generated automatically.
3. Click **Apply**. On first boot the container runs `flask db upgrade` to create the schema, then serves on Render's port. Wait for the health check (`/api/health`) to go green, then open the URL — it's your MiniMart landing page.

**C. Demo data (optional, wipes and recreates tables)**
Render dashboard → your service → **Shell** → `python scripts/seed.py` → log in as `john@gmail.com` / `customer123`.

**Free-tier caveats:** the service sleeps after 15 minutes idle (first request after a nap takes ~30–60s — normal); Aiven's free node has no SLA/backups; the chat needs `GROQ_API_KEY` or it returns a "temporarily unavailable" message. Render's free Postgres expires after 90 days — don't use it here; this setup uses Aiven MySQL instead.

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
