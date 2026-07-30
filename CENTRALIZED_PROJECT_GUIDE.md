# SafeBite - Centralized Project Documentation

## 🎯 Project Overview

**SafeBite** is a restaurant discovery platform focused on **food safety transparency**. The core feature is displaying comprehensive inspection history for every restaurant.

### Key Philosophy
- **Inspection History is THE MAIN FEATURE**
- **CSV files are the single source of truth** 
- **One centralized database** created from CSV data
- **Complete inspection timeline** with violations, inspectors, and corrective actions

---

## 📁 Project Structure

```
d:\safebite\
├── data\                          # 📊 SINGLE SOURCE OF TRUTH (CSV FILES)
│   ├── restaurants.csv           # Restaurant basic info
│   ├── inspections.csv           # Inspection records
│   ├── inspectors.csv            # Health department inspectors
│   ├── violations.csv            # Violation records
│   ├── violation_codes.csv       # Standard FDA violation codes
│   └── users.csv                 # User accounts
├── database\                     # 💾 Generated database
│   └── safebite.db               # SINGLE SQLite database (auto-generated)
├── backend\                      # 🚀 FastAPI Backend
│   └── app\
│       ├── api\                  # API endpoints
│       ├── core\                 # Config, database, security
│       ├── models\               # SQLAlchemy models
│       ├── schemas\              # Pydantic schemas
│       └── main.py               # App entry point
├── frontend\                     # 💻 React Frontend
│   └── src\
│       ├── components\           # React components
│       ├── pages\                # Page components
│       ├── services\             # API service
│       └── context\              # Auth context
├── docs\                         # 📚 Documentation
└── create_database_from_csv.py   # 🔧 Database creator script
```

---

## 🗄️ Database Architecture

### Single Source of Truth: CSV Files

**Location**: `d:\safebite\data\*.csv`

All data originates from CSV files in the `/data` directory:

#### **restaurants.csv**
```csv
RestaurantID,RestaurantName,Cuisine,Address,City,State,Phone,Email,OwnerName,LicenseNumber,LicenseStatus,RestaurantStatus,SafetyScore,SafetyRating
R0001,Sakura Sushi Bar,Japanese,123 Main Street,Austin,Texas,555-0101,owner1@safebite.demo,Takeshi Yamamoto,LIC-123456,Active,Open,85,Good
```

#### **inspections.csv**
```csv
InspectionID,RestaurantID,InspectorID,InspectionDate,InspectionType,DurationMinutes,TotalScore,PassFailStatus,RiskLevel,InspectorNotes
INS001,R0001,1,2024-03-15,Routine,90,85,Passed with Violations,Medium,Food temperature issues noted
```

#### **violations.csv**
```csv
ViolationID,InspectionID,ViolationCode,Category,Description,Location,Severity,PointsDeducted,CorrectedOnSite,HealthRiskLevel
V001,INS001,3-501.16,Temperature Control,Food temperature not maintained at safe levels,Cold Storage,Major,5,False,High
```

### Database Creation Process

1. **Run the database creator**:
   ```bash
   python create_database_from_csv.py
   ```

2. **What it does**:
   - Reads all CSV files from `/data` directory
   - Drops existing database tables
   - Creates fresh SQLite database at `d:\safebite\database\safebite.db`
   - Establishes all relationships between tables

3. **Result**: Single database file with complete relational structure

### Database Tables

The CSV data is transformed into these SQLAlchemy tables:

1. **users** - User accounts (admin, customer, owner)
2. **restaurants** - Restaurant information and safety scores  
3. **restaurant_images** - Restaurant photos
4. **inspectors** - Health department inspectors
5. **inspections** - Inspection records with scores and notes
6. **violation_codes** - Standard FDA violation codes
7. **violations** - Specific violations found during inspections
8. **inspection_photos** - Photos taken during inspections
9. **complaints** - Public complaints about restaurants

---

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.12
- **Framework**: FastAPI (async web framework)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens + bcrypt
- **Validation**: Pydantic schemas
- **Server**: Uvicorn ASGI server
- **Port**: 8000

### Frontend  
- **Language**: JavaScript/React 18
- **Build Tool**: Vite (fast development)
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Port**: 3001 (proxies to backend:8000)

---

## 🔄 Project Flow & Startup

### Complete Startup Process

#### Step 1: Create Database (REQUIRED FIRST)
```bash
cd d:\safebite
python create_database_from_csv.py
```
**Result**: Creates `d:\safebite\database\safebite.db` from CSV files

#### Step 2: Start Backend
```bash
cd d:\safebite\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
**Result**: Backend API available at http://localhost:8000

#### Step 3: Start Frontend  
```bash
cd d:\safebite\frontend
npm run dev
```
**Result**: Frontend available at http://localhost:3001

### File Execution Order

1. **create_database_from_csv.py** - Creates database from CSV
2. **backend/app/main.py** - FastAPI application entry point
3. **frontend/src/main.jsx** - React application entry point

---

## 🚀 Backend Details

### Entry Point
- **File**: `backend/app/main.py`
- **Framework**: FastAPI application
- **CORS**: Enabled for frontend communication
- **Auto-docs**: Available at http://localhost:8000/docs

### API Structure
```
/api/auth/*                    # Authentication endpoints
/api/restaurants/*             # Restaurant CRUD + inspection data
/api/admin/*                   # Admin management endpoints  
/api/violation-codes           # FDA violation code reference
/api/inspectors                # Inspector information
```

### Key Backend Files
- `app/main.py` - FastAPI app configuration and route registration
- `app/core/config.py` - Database URL and app settings
- `app/core/database.py` - SQLAlchemy database connection
- `app/models/models.py` - Database table definitions
- `app/api/inspections.py` - **MAIN FEATURE** - Inspection history API
- `app/api/restaurants.py` - Restaurant CRUD operations
- `app/api/auth.py` - JWT authentication system

### Database Connection
```python
# From app/core/config.py
DATABASE_URL = "sqlite:///d:/safebite/database/safebite.db"
```

---

## 💻 Frontend Details

### Entry Point
- **File**: `frontend/src/main.jsx`
- **Router**: React Router manages page navigation
- **Auth**: Context-based authentication state

### Key Frontend Files
- `src/main.jsx` - React app initialization
- `src/App.jsx` - Main app component with routing
- `src/components/InspectionHistory.jsx` - **MAIN FEATURE** - Rich inspection timeline
- `src/pages/RestaurantDetail.jsx` - Restaurant page with inspection focus
- `src/pages/RestaurantListing.jsx` - Restaurant browsing with safety scores
- `src/services/api.js` - Axios API communication layer

### Component Architecture
```
App.jsx
├── Home.jsx (landing page)
├── RestaurantListing.jsx (browse restaurants)
├── RestaurantDetail.jsx (restaurant page)
│   └── InspectionHistory.jsx (THE MAIN FEATURE)
├── LoginRegister.jsx (authentication)
├── OwnerDashboard.jsx (restaurant management)
└── AdminDashboard.jsx (admin controls)
```

### API Integration
- **Proxy**: Vite proxies `/api/*` to `localhost:8000`
- **Authentication**: JWT tokens stored in localStorage
- **Error Handling**: Automatic token refresh and logout

---

## 🎯 Main Feature: Inspection History

### Why This is THE Core Feature
The entire project centers around making restaurant inspection history highly visible and detailed.

### Frontend Component: InspectionHistory.jsx
- **Interactive timeline** of all inspections
- **Expandable details** for each inspection
- **Violation breakdown** by severity (Critical/Major/Minor)
- **Inspector credentials** with badges and departments
- **Visual indicators** for pass/fail status
- **Color-coded risk levels** and violation types

### API Endpoint: `/api/restaurants/{id}/inspections`
Returns complete inspection timeline with:
- Inspector information (name, badge, certification)
- Violation details with FDA codes
- Correction status (on-site vs follow-up required)
- Risk assessments and health impact
- Photos and documentation

### Data Flow
```
CSV files → Database → API → Frontend Component → User Interface
```

---

## 🔧 How to Run (Simple Steps)

### One-Time Setup
```bash
cd d:\safebite
python create_database_from_csv.py  # Creates database from CSV
```

### Every Time
```bash
# Terminal 1 - Backend
cd d:\safebite\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend  
cd d:\safebite\frontend
npm run dev
```

### Access
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🎭 Demo Accounts

From `data/users.csv`:

- **Admin**: admin@safebite.demo / password123
- **Customer**: customer@safebite.demo / password123  
- **Owner**: owner1@safebite.demo / password123

---

## 🔍 Testing the Main Feature

1. Open http://localhost:3001
2. Browse to any restaurant (e.g., "Sakura Sushi Bar")
3. **Inspection History tab loads by default** ⭐
4. Click on any inspection to see:
   - Inspector details (Dr. Sarah Chen, Badge INS-001)
   - Violation details with FDA codes
   - Severity levels and health risks
   - Correction status and deadlines

---

## ✨ Key Benefits of This Approach

### 1. **CSV as Source of Truth**
- Easy to edit and understand
- Version controllable
- Human readable
- Can be exported from any system

### 2. **Single Database**
- No confusion about which DB to use
- Clean, predictable location
- Rebuilds fresh every time

### 3. **Inspection-Focused Design**
- Every restaurant page defaults to inspection tab
- Rich violation details with FDA codes
- Professional inspector information
- Visual timeline interface

This system makes food safety transparency the star of the show! 🌟