# Customer-rep

GBOLAGADE's MiniMart — a support assistant: Gradio Support AI Assistant (text + voice) powered by Groq and MySQL. The entry point is `run.py`, which launches the Gradio assistant; the Flask API in `app/` is independent and runs separately if needed.

## Stack

| Layer    | Tech                                                        |
|----------|-------------------------------------------------------------|
| Backend  | Gradio assistant UI (python run.py) + optional Flask API in app/ |
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

Open http://localhost:7860 — the Gradio assistant UI. (With MySQL instead of SQLite, unset `DATABASE_URL` and set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.)

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

Then reach the API:

- Gradio AI assistant: http://localhost:7860 (log in as `john@gmail.com` / `customer123` after seeding at the /api/login endpoint if the Flask API is running)

### Services

| Service  | Port | Purpose                                     |
|----------|------|---------------------------------------------|
| backend  | 7860 | Gradio Support AI assistant (`python run.py`) |
| db       | —    | MySQL 8 (volume `db_data`)                  |

`docker compose down -v` removes the database volume too.

## Deploy everything on Railway (one place)

Everything runs as **one web service** exposing the API (`/api/*`) plus **one MySQL plugin** in the same project. The optional Gradio UI can be a second service.

1. Push this repo to GitHub (already done).
2. At railway.app: **New Project → Deploy from GitHub repo** → pick `BugClasiq/Customer-rep`.
3. **+ New → Database → MySQL**.
4. On the web service's **Variables** tab:
   - `DATABASE_URL` — reference the plugin (e.g. `${{MySQL.MYSQL_URL}}`); cloud plugins hand out `mysql://...`, and this app rewrites it to `mysql+pymysql://...` automatically.
   - `SECRET_KEY`, `JWT_SECRET_KEY` — any long random strings.
   - `GROQ_API_KEY` — required for the AI chat (`/api/chat`).
5. Railway builds the repo-root **Dockerfile** (`python run.py` → Gradio assistant on `$PORT` by default) and applies migrations on boot when `DATABASE_URL` is set (otherwise it boots anyway). Set the service's **healthcheck path to `/`**.
6. **Networking → Generate Domain** → open it. The **Domain root serves the Gradio assistant** ("Support AI Assistant") — sign in isn't required. Open http://localhost:7860 locally, or `https://<your-domain>` on Railway.
7. Demo data: open a **Shell** on the service and run `python scripts/seed.py` (drops and recreates all tables). Log in as `john@gmail.com` / `customer123`.
8. Optional Gradio UI: **+ New → GitHub repo** (same repo) → **Root Directory** `backend`, **Custom Start Command** `python ai/main.py`, variable `GRADIO_SERVER_NAME=0.0.0.0`. It binds Railway's `$PORT` automatically. Text chat works; mic input additionally requires `pip install -r requirements-voice.txt`, which needs native audio libraries.

Note: Railway is not free — you get trial credit and the MySQL plugin consumes credits (usage-based, a few dollars/month).

## Deploy everything on Render (free)

One Render web service (free tier) serves the API (`/api/*`). MySQL comes from [Aiven's](https://aiven.io/free-mysql) free tier (Render has no free MySQL); the code rewrites its `mysql://` URL for you.

**A. Get a free MySQL (5 minutes)**
1. Sign up at aiven.io → **New project? → Free MySQL** → create the free plan.
2. Once running, copy the **Connection URI** (`mysql://user:password@host:port/defaultdb`).

**B. Deploy the app**
1. render.com → **New → Blueprint** → connect your GitHub repo → select `BugClasiq/Customer-rep`.
2. Render reads `render.yaml` and asks for `DATABASE_URL` (paste the Aiven URI) and `GROQ_API_KEY` (from console.groq.com). `SECRET_KEY`/`JWT_SECRET_KEY` are generated automatically.
3. Click **Apply**. On first boot the container runs `flask db upgrade` (when `DATABASE_URL` is set) to create the schema, then serves the Gradio assistant on Render's port. Wait for the health check (`/`) to go green, then open the URL — it shows the Support AI Assistant.

**C. Demo data (optional, wipes and recreates tables)**
Render dashboard → your service → **Shell** → `python scripts/seed.py` → log in as `john@gmail.com` / `customer123`.

**Free-tier caveats:** the service sleeps after 15 minutes idle (first request after a nap takes ~30–60s — normal); Aiven's free node has no SLA/backups; the chat needs `GROQ_API_KEY` or it returns a "temporarily unavailable" message. Render's free Postgres expires after 90 days — don't use it here; this setup uses Aiven MySQL instead.

## Environment variables

See `.env.example`. `GROQ_API_KEY` is required for the AI assistant to answer (`/api/chat` and the Gradio UI) - without it, chat returns HTTP 503 / an error bubble; everything else works. Set `GROQ_MODEL` to override the default `openai/gpt-oss-120b`.

For local (non-Docker) runs, run the assistant with `cd backend && set DATABASE_URL=sqlite:///dev.db && python run.py` and open http://localhost:7860. Create the schema with `flask --app app:create_app() db upgrade` (works for SQLite too), or just run `python scripts/seed.py` to drop/recreate everything and load the demo data. The Flask API in `app/` runs separately (`flask --app app:create_app() run`) if you need `/api/*` — it is not started by `run.py`.

## Voice features (optional)

The Gradio assistant supports mic input / spoken replies, but those native dependencies are **not** installed by default:

```bash
pip install -r backend/requirements-voice.txt
```

They need a C toolchain and platform audio libraries (e.g. `portaudio19-dev`). Without them, text chat in the Gradio UI and `/api/chat` work normally; voice buttons degrade gracefully.

## Project layout

```
backend/
  app/       Flask app factory, extensions, models, routes (auth, chat, health)
  ai/        Intent detection, Groq provider, response engine, speech, Gradio UI
  migrations/ Alembic migrations
  scripts/   seed.py (demo data), test.py (interactive order-CLI)
  run.py     Entry: Gradio Support AI Assistant (gunicorn is no longer used)
Dockerfile          Whole-app image: python run.py → Gradio assistant on $PORT (Railway/Render)
docker-compose.yml  MySQL + assistant (python run.py)
render.yaml         Render Blueprint (free, one web service)
```

## Known limitations / notes

- Passwords: bcrypt, ≥8 chars enforced on signup. Emails are stored lowercase.
- `/api/chat` creates a new Groq API call per message; there is no rate limiting.
- The chat page requires `GROQ_API_KEY` and the seeded knowledge base to give useful answers.
- JWTs are wired (`flask-jwt-extended`) but nothing issues tokens yet — auth responses are plain JSON for now.
- `scripts/seed.py` is destructive (drops all tables). Don't run it against a database you care about.
