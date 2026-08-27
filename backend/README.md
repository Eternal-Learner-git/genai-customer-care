# Backend — GenAI Customer Care System

FastAPI backend handling authentication, complaint/ticket CRUD, and the database layer.
This is the API that the RAG engine, NLP engine, and React frontend all connect to.

## What's included

- **JWT authentication** — register, login, and a protected `/me` endpoint
- **Complaint CRUD** — create, list, view, update, delete
- **Role-based access** — `customer` vs `admin` (admins see all complaints and can update/delete)
- **MySQL via SQLAlchemy** — models for `User` and `Complaint`
- Fields on `Complaint` (`category`, `sentiment`, `priority`, `suggested_response`) are left nullable
  and empty for now — the NLP engine and RAG engine will fill these in via the `PATCH /complaints/{id}`
  endpoint once they're built.

## Setup

1. **Create a MySQL database** (using MySQL Workbench, the CLI, or SQLTools in VS Code):
   ```sql
   CREATE DATABASE complaint_db;
   ```

2. **Create a virtual environment** inside the `backend/` folder:
   ```bash
   python -m venv venv
   ```
   Activate it:
   - Windows (PowerShell): `venv\Scripts\Activate.ps1`
   - Mac/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your real MySQL password and a random secret key:
   ```bash
   cp .env.example .env
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   The API will be running at `http://localhost:8000`.

6. **Explore and test it:**
   Open `http://localhost:8000/docs` in your browser — FastAPI auto-generates an interactive
   Swagger UI where you can try every endpoint (register a user, log in, create complaints) without
   needing the frontend built yet.

## Typical flow to test manually

1. `POST /register` — create a user (name, email, password)
2. `POST /token` — log in with that email/password (form fields: `username` = email, `password`) → get back an access token
3. Click "Authorize" in `/docs` and paste the token
4. `POST /complaints` — create a complaint as that logged-in user
5. `GET /complaints/me` — see your own complaints

To test the admin-only endpoints, manually set a user's `role` to `admin` in the database
(there's no signup flow for admins yet — that's intentional, admins should be provisioned directly).

## Folder structure

```
backend/
├── main.py          # FastAPI app + all route definitions
├── database.py       # DB engine/session setup
├── models.py          # SQLAlchemy ORM models (User, Complaint)
├── schemas.py         # Pydantic request/response schemas
├── crud.py            # DB query functions
├── auth.py            # Password hashing + JWT logic
├── requirements.txt
├── .env.example
└── README.md
```

## Next integration points (for later weeks)

- **NLP engine** will call `PATCH /complaints/{id}` to fill in `category`, `sentiment`, `priority`
  after classifying a new complaint.
- **RAG engine** will call the same endpoint to fill in `suggested_response`.
- **Frontend** will call `/register`, `/token`, `/complaints`, and `/complaints/me` directly.
