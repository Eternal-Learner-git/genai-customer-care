# Frontend — GenAI Customer Care System

React + Vite + Tailwind app: a customer complaint portal and an admin dashboard,
both talking to the FastAPI backend built earlier.

## What's included

- **Login / Register** — connects to the backend's `/token` and `/register` endpoints
- **Customer dashboard** (`/`) — submit a new complaint, see your own complaint history
  including category/sentiment/priority once the NLP engine is wired in, and the
  AI-suggested response once the RAG engine is wired in
- **Admin dashboard** (`/admin`, admin accounts only) — view every complaint, filter by
  status, update status and priority inline
- **Auth context** — JWT stored in `localStorage`, attached automatically to every API
  request, with route protection so `/` and `/admin` redirect to `/login` if not authenticated

## Design notes

The palette and type choices are deliberate for a medical complaint system, not the
default AI-generated look:
- **Deep teal** as the primary color — calm, clinical-but-warm, avoids both the
  cliché cream+terracotta and dark+neon AI aesthetic
- **Coral** reserved *only* for high/critical priority badges, so it stays meaningful
  instead of decorative
- **Newsreader** (serif) for page titles only, paired with **Inter** for all UI/body
  text — gives page headers some character without sacrificing dashboard readability

## ⚠️ This is not yet wired to the NLP/RAG engines

Right now, when a customer submits a complaint, it's created via `POST /complaints`
exactly as the backend already supports - `category`, `sentiment`, `priority`, and
`suggested_response` will show as empty/default until the backend is updated to call
the NLP and RAG engines and `PATCH` those fields in. The UI already has the display
logic ready for when that data exists (see `ComplaintCard.jsx` and `AdminDashboard.jsx`)
- nothing in the frontend needs to change for that integration.

## Setup

1. **Install Node.js** if you haven't already (v18+): [nodejs.org](https://nodejs.org)

2. **Install dependencies** inside `frontend/`:
   ```bash
   npm install
   ```

3. **Configure the API URL** (only needed if your backend isn't on the default):
   ```bash
   cp .env.example .env
   ```

4. **Make sure the backend is running** in a separate terminal:
   ```bash
   # in the backend/ folder, with its own venv active
   uvicorn main:app --reload
   ```

5. **Run the frontend:**
   ```bash
   npm run dev
   ```
   Open the URL it prints (typically `http://localhost:5173`).

## Testing it end to end

1. Go to `/register`, create a customer account
2. You'll land on `/` — submit a test complaint, confirm it appears below the form
3. To test the admin view: register a second account, then manually set that user's
   `role` to `admin` in MySQL (there's no admin signup flow by design - see the
   backend README), log in as that user, and visit `/admin`
4. Confirm you can change a complaint's status/priority from the admin dashboard and
   see it update immediately

## Folder structure

```
frontend/
├── src/
│   ├── api/client.js            # axios instance, attaches JWT automatically
│   ├── context/AuthContext.jsx    # login/register/logout state, persisted token
│   ├── components/
│   │   ├── Navbar.jsx               # top nav, shows admin link only for admins
│   │   ├── ProtectedRoute.jsx         # redirects unauthenticated/non-admin users
│   │   ├── Badges.jsx                   # priority/status color-coded badges
│   │   └── ComplaintCard.jsx              # single complaint display
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── CustomerDashboard.jsx            # submit + view own complaints
│   │   └── AdminDashboard.jsx                 # view all, update status/priority
│   ├── App.jsx                                  # routes
│   ├── main.jsx                                   # entry point
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── .env.example
```
