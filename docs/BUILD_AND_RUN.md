# SafeBite — Build, Run & Deployment Guide

**Version:** 1.0.0  
**Target Environments:** Local Workstation (Windows, macOS, Linux) & Docker Containerized  

---

## 1. Prerequisites

Ensure the following runtimes are installed on your host system:
- **Python:** Version 3.10, 3.11, or 3.12 (tested on 3.12.4)
- **Node.js:** Version 18.x or 20.x (tested on Node 20.x with npm 10.x)
- **Docker & Docker Compose:** (Optional, for containerized run)

---

## 2. Local Setup (Without Docker)

### 2.1 Backend Initialization
```bash
# 1. Navigate to backend directory
cd backend

# 2. Create and activate a Python virtual environment
python -m venv venv

# On Windows (PowerShell/CMD):
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt reportlab selenium

# 4. Migrate database schema (adds provenance fields and correction_requests table)
python migrate_db.py

# 5. Ingest verified inspection records
python ingest_inspection_data.py

# 6. Start FastAPI development server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

*Verification:*  
Open a separate terminal and test the health endpoint:
```bash
curl http://127.0.0.1:8000/api/health
# Expected Output: {"status":"healthy","app":"SafeBite","version":"1.0.0 (Review 1 MVP)"}
```

### 2.2 Frontend Initialization
```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install NPM dependencies
npm install

# 3. Build production bundle (sanity check)
npm run build

# 4. Start Vite development server
npm run dev
```

*Verification:*  
Open your browser to: `http://127.0.0.1:5173/`

---

## 3. Docker Compose Orchestration

To run the entire platform as isolated containers with unified networking:

```bash
# From the repository root:
docker-compose up --build
```

### Container Services:
| Service | Container Name | Host Port | Internal Port | Health Probe |
|---|---|---|---|---|
| `backend` | `safebite-backend-1` | `8000` | `8000` | `http://localhost:8000/api/health` |
| `frontend` | `safebite-frontend-1` | `3000` | `80` (Nginx) | `http://localhost:3000/` |

To stop the containers:
```bash
docker-compose down
```

---

## 4. Automated Testing Execution

Verify platform integrity with the automated test suites:
```bash
cd backend
# Run full Pytest test suite (23 tests)
pytest -v

# Run mutation testing suite (7 mutants)
python tests/run_mutation_testing.py
```

---

## 5. Troubleshooting & FAQ

### Port 8000 or 5173 already in use:
- **Windows:** Run `netstat -ano | findstr :8000` and terminate the PID with `taskkill /F /PID <pid>`.
- **macOS/Linux:** Run `lsof -i :8000` and kill with `kill -9 <pid>`.

### SQLite database locked error:
- Ensure no lingering background Python uvicorn processes are concurrently holding write locks. Restart the server cleanly.

### CORS error when connecting to API:
- The FastAPI CORS middleware in `backend/app/main.py` is configured with `allow_origins=["*"]`, allowing requests from `http://127.0.0.1:5173`, `http://localhost:3000`, and Chrome extension origins.
