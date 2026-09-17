# Camp Moses Academy — Local server scaffold

This scaffold provides a minimal Node.js + Express server that serves the existing `index.html` and `img/` folder, plus a small SQLite-backed API example.

Quick start

1. Install Node.js (v16+ recommended).
2. From the project folder, install dependencies:

```bash
npm install
```

3. Start the server:

```bash
npm start
```

The site will be served at http://localhost:3000 and the example API endpoints are:

- `GET /api/notes` — list notes
- `POST /api/notes` — create note { "content": "..." }
- `GET /api/health` — health check

Notes
- Database file is created at `data/app.db` automatically.
- If `sqlite3` install fails on Windows, install the required build tools or let me switch the scaffold to a file-based JSON store instead.

Python alternative
------------------
I also added a minimal Python (Flask) server that provides the same functionality and can be run with `python server.py`.

Quick start (Python)

```powershell
python -m venv venv
venv\Scripts\Activate
pip install -r requirements.txt
python server.py
```

The Python server listens on `http://localhost:8000` by default and exposes:

- `GET /api/health`
- `GET /api/notes`
- `POST /api/notes` — JSON `{ "content": "..." }`

