# SafeBite - Complete Project Documentation

## 📋 Table of Contents
1. Project Overview
2. Tech Stack
3. Database Architecture
4. Project Flow & Startup
5. Backend Details
6. Frontend Details
7. Key Files & Directories
8. How to Run

---

## 🎯 Project Overview

**SafeBite** is a restaurant discovery and food safety transparency platform that helps customers make informed dining decisions based on inspection history and safety records.

### Core Features
- Restaurant browsing with real-time inspection history
- Food safety score tracking (0-100)
- Detailed violation records with severity levels
- Inspector information and credibility
- Admin approval workflow
- User authentication (Customer, Owner, Admin roles)

### Main Goal
**Make inspection history the MAIN feature** - Every restaurant should display complete inspection timeline with violations, photos, and corrective actions.

---

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.12
- **Framework**: FastAPI 0.115.14 (async web framework)
- **Database ORM**: SQLAlchemy (database abstraction)
- **Database**: SQLite (development) / PostgreSQL-ready
- **Authentication**: JWT tokens + bcrypt password hashing
- **Validation**: Pydantic (data validation)
- **Server**: Uvicorn (ASGI server)
- **Port**: 8000

### Frontend
- **Language**: JavaScript (ES6+)
- **Framework**: React 18
- **Build Tool**: Vite 4.5.14 (fast build system)
- **Styling**: Tailwind CSS (utility-first CSS)
- **Routing**: React Router v6
- **HTTP Client**: Axios (API communication)
- **Icons**: Lucide React
- **State Management**: React Context API
- **Port**: 3001 (Vite dev server)

---

## 🗄️ Database Architecture

### Database File Location
```
d:\safebite\database\safebite_v2.db
```

### Database Type
- **SQLite** (file-based, development-friendly)
- Located in: `d:/safebite/database/safebite_v2.db`
- Created by: `create_test_inspection_db.py` script

### Source of Truth
The database is created fresh each time by running the seed script:
```bash
python create_test_inspection_db.py
```

This script:
1. Drops all existing tables
2. Creates fresh schema from SQLAlchemy models
3. Seeds with 100 test restaurants (from CSV)
4. Creates 3 inspectors
5. Generates 2-3 inspections per restaurant
6. Adds violations and violation codes