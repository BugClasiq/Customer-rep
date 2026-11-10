# Support AI Backend Study Guide

## Overview
This backend project is a Flask-based support assistant service with database models, authentication, and AI-driven intent detection.

## Project Structure
- `run.py`
  - Launches the Flask application using `create_app()` from `app/__init__.py`.
- `config.py`
  - Loads environment variables from `.env`.
  - Configures database URI and secret keys.
- `app/`
  - Contains the Flask application factory, extensions, models, and routes.
  - `app/__init__.py` sets up the Flask app, config, extensions, and blueprint registration.
  - `app/extension.py` defines shared Flask extensions: `db`, `jwt`, and `migrate`.
  - `app/routes/auth.py` provides authentication endpoints for login and signup.
  - `app/models/` contains ORM models for users, products, orders, tickets, and knowledge base entries.
- `ai/`
  - Contains the AI helper code for intent detection and response generation.
  - `ai/groq_provider.py` wraps the Groq API client.
  - `ai/intent_detector.py` classifies user messages into intents.
  - `ai/engine.py` builds context, queries the database, and generates AI responses.
- `requirements.txt`
  - Lists core dependencies: `flask`, `flask-sqlalchemy`, `flask-migrate`, and `flask-cors`.

## Architecture Diagram

```text
                +--------------------------+
                |  Client / Frontend App   |
                +-----------+--------------+
                            |
                            | HTTP requests
                            v
                +--------------------------+
                |       Flask Backend      |
                |   (`run.py` -> `app`)    |
                +-----------+--------------+
                            |
            +---------------+---------------+
            |                               |
            v                               v
+-------------------------+       +-------------------------+
|  Auth routes (`/api/`)  |       |  AI Engine (`ai/`)      |
|  `app/routes/auth.py`   |       |  `engine.py`            |
+------------+------------+       +------------+------------+
             |                                 |
             v                                 v
       +------------+                 +-----------------------+
       |  Database  |                 |  LLM Provider (Groq)  |
       |  MySQL     |                 |  `ai/groq_provider.py`|
       +------------+                 +-----------------------+
             ^                                 ^
             |                                 |
+------------+------------+        +-----------+----------------+
|  ORM Models (`app/models`) |      |  Intent Detector (`ai/intent_detector.py`) |
+---------------------------+      +-------------------------------------------+
```

## Key Workflow
1. **Start application**
   - Run `python run.py`
   - Flask app starts with debug mode enabled.

2. **App initialization**
   - `create_app()` loads configuration and initializes database and migration extensions.
   - CORS is enabled.
   - The auth blueprint is registered under `/api`.

3. **Authentication**
   - `POST /api/login`
     - Validates email and password against `User` records.
   - `POST /api/signup`
     - Validates signup fields and checks for existing users.
     - Note: signup logic is incomplete and needs user creation implementation.

4. **AI request handling (engine-only)**
   - `ai/engine.py` receives a user message and optional chat history.
   - Detects intent using `ai/intent_detector.py`.
   - Retrieves relevant context from the database:
     - products for `product_query`
     - orders for `order_query`
     - knowledge base entries for `knowledge_query`
   - Builds a prompt and sends it to Groq via `ai/groq_provider.py`.
   - Returns the AI-generated response and updated chat history.

## Important Notes
- The backend currently has only auth routes exposed via Flask.
- The AI engine is implemented but not yet connected to an HTTP endpoint.
- `.env` must contain database and API credentials for full functionality.
- `ai/groq_provider.py` expects `GROQ_API_KEY` and optionally `GROQ_MODEL`.

## Study Recommendations
- Review `app/models/` to understand schema relationships and database structure.
- Inspect `ai/engine.py` to see how intent and context are combined into an LLM prompt.
- Improve `app/routes/auth.py` signup endpoint by adding user creation logic and password hashing.
- Add a Flask route for AI chat if you want the AI engine accessible through HTTP.

## Quick Mapping
- `run.py` → app entrypoint
- `app/__init__.py` → Flask factory
- `config.py` → env config
- `app/extension.py` → shared extensions
- `app/routes/auth.py` → auth endpoint handlers
- `ai/groq_provider.py` → LLM provider client
- `ai/intent_detector.py` → intent classification module
- `ai/engine.py` → AI response workflow
