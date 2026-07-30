# SafeBite - Restaurant Food Safety Transparency Platform

A comprehensive platform for discovering restaurants with verified food safety standards and transparent inspection histories.

## 📋 1. Vision Document

### Project Name & Overview
**SafeBite** is a restaurant discovery platform that prioritizes food safety transparency, helping customers make informed dining decisions based on comprehensive inspection histories, safety scores, and violation records from FSSAI health department data.

### Problem it Solves
- **Lack of Food Safety Transparency**: Customers have no easy access to inspection histories
- **Hidden Violation Records**: Critical health violations buried in government databases
- **Uninformed Dining Decisions**: People cannot assess food safety risks before visiting
- **Scattered Safety Information**: Inspection data and violation codes are not centralized

### Target Users (Personas)
| Persona | Role / Age | Goal | Pain Point |
|---------|------------|------|------------|
| **Sarah** | Health-Conscious Customer, 32 | Find restaurants with excellent safety records for family dining | Cannot easily access inspection histories |
| **Mike** | Restaurant Owner, 45 | Showcase excellent safety practices and improve visibility | Customers do not see safety improvements |
| **Lisa** | Health Inspector, 38 | Ensure restaurants maintain safety standards | Limited public visibility of inspection data |

### Vision Statement
*"To create a transparent ecosystem where food safety information is accessible, empowering customers to make informed dining decisions while helping restaurants showcase their commitment to health standards."*

### Key Features / Goals
1. **Comprehensive Inspection History** - Complete timeline of all inspections with violation details
2. **Real-time Safety Scores** - 0-100 safety ratings based on latest FSSAI inspections
3. **Violation Transparency** - Detailed FSSAI violation codes with corrective actions
4. **Inspector Credibility** - Health inspector profiles with credentials and experience
5. **Restaurant Discovery** - Advanced filtering by safety scores, cuisine, and location
6. **Admin Approval Workflow** - Quality control for restaurant listings
7. **Mobile-Responsive Design** - Accessible on all devices

### Success Metrics
| Metric | Target |
|--------|--------|
| **User Engagement** | 80%+ of users check inspection history before restaurant visits |
| **Data Accuracy** | 95%+ accuracy in safety score calculations |
| **Restaurant Adoption** | 500+ restaurants onboarded in first 6 months |
| **Customer Trust** | 4.5+ star average app rating |
| **Health Impact** | 20% reduction in food poisoning reports in coverage areas |

---

## 📝 2. User Stories (25 GitHub Issues)

All 25 user stories have been tracked in the GitHub Issues section of this repository. They are grouped into 7 main Epics:
1. **Epic 1: Authentication & Management** (3 Stories)
2. **Epic 2: Restaurant Search & Discovery** (4 Stories)
3. **Epic 3: Food Safety & Inspection History** (5 Stories)
4. **Epic 4: Restaurant Owner Management** (4 Stories)
5. **Epic 5: Admin Management** (4 Stories)
6. **Epic 6: User Experience** (3 Stories)
7. **Epic 7: Data Management** (2 Stories)

---

## 🎯 3. MoSCoW Prioritization

### Must Have (Critical for MVP)
- Story 1 - User Registration
- Story 2 - User Login
- Story 4 - Browse Restaurant Listings
- Story 7 - View Restaurant Details
- Story 8 - View Safety Score
- Story 9 - View Inspection History Timeline
- Story 13 - Create Restaurant Listing
- Story 17 - Review Pending Applications
- Story 18 - Approve Restaurant Listings
- Story 21 - Responsive Mobile Design
- Story 24 - CSV Data Import System

### Should Have (Important for User Experience)
- Story 3 - Role-Based Access Control
- Story 5 - Filter Restaurants by Criteria
- Story 6 - Search Restaurants by Name
- Story 10 - View Inspection Violation Details
- Story 14 - Edit Restaurant Information
- Story 15 - View Listing Approval Status
- Story 19 - Reject Restaurant Listings
- Story 22 - Navigation and Site Structure
- Story 23 - Loading States & Performance

### Could Have (Nice to Have Features)
- Story 11 - View Inspector Information
- Story 12 - View Violation Photos
- Story 16 - Manage Multiple Locations
- Story 20 - Manage Users
- Story 25 - Data Synchronization with Health Departments

### Won't Have (Future Releases)
- Advanced Analytics Dashboard
- Live Notifications
- Mobile Application
- Customer Review System

---

## 🎨 Figma Wireframes
[View Figma Wireframes Here](https://www.figma.com/design/bKqw8mWVk8IHUb1oXcNMG2/Untitled?node-id=0-1&p=f&t=ayZDpOpgXNiVLV9q-0)

Includes screens for:
1. Login / Sign Up
2. Home Page
3. Restaurant Details
4. Owner Dashboard
5. Admin Dashboard

---

## 🏗️ 4. Architecture

SafeBite follows a modern web architecture:
**Frontend (React)** → **Backend (FastAPI)** → **Database (SQLite)** → **Deployment (Docker)**

### Tech Stack
| Layer | Technology | Port |
|-------|------------|------|
| **Frontend** | React 18, Vite, Tailwind CSS, Axios | 3001 |
| **Backend** | FastAPI, Python 3.12, Uvicorn, JWT | 8000 |
| **Database** | SQLite, SQLAlchemy ORM | - |
| **DevOps** | Docker, Docker Compose | - |

---

## 🚀 5. Development Setup & Quick Start

### Folder Structure
```text
safebite/
├── frontend/                 # React 18 + Vite + Tailwind CSS
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── backend/                  # FastAPI + Python 3.12
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── database/                 # Contains pre-seeded SQLite database
│   └── safebite.db           # 1,000+ Indian restaurants pre-loaded
├── docs/                     # Documentation
├── .gitignore                # Rules for version control
├── docker-compose.yml        # Docker orchestration
└── README.md
```

### Run Locally (Docker)
Ensure **Docker Desktop** is installed and running.

```bash
git clone https://github.com/rudransh27sharma/SafeBite.git
cd SafeBite
docker-compose up --build
```

**Access URLs:**
- **Frontend App:** http://localhost:3001
- **Backend API Docs (Swagger):** http://localhost:8000/docs

*Note: The SQLite database comes fully pre-seeded out of the box.*

### Branching Strategy (GitHub Flow)
1. **main** - Production-ready code
2. **feature/[name]** - Short-lived feature branches (e.g., `feature/docker-setup`)
3. Open a Pull Request → Review → Squash & Merge

---

## 🔑 Demo Accounts
- **Admin**: admin@safebite.demo / password123
- **Customer**: customer@safebite.demo / password123  
- **Restaurant Owner**: owner1@safebite.demo / password123