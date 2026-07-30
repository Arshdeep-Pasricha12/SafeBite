# SafeBite - Restaurant Food Safety Transparency Platform

A comprehensive platform for discovering restaurants with verified food safety standards and transparent inspection histories.

## 📋 Vision Document

### Project Name & Overview
**SafeBite** is a restaurant discovery platform that prioritizes food safety transparency, helping customers make informed dining decisions based on comprehensive inspection histories, safety scores, and violation records from health department data.

### Problem it Solves
- **Lack of Food Safety Transparency**: Customers have no easy way to access restaurant inspection histories
- **Hidden Violation Records**: Critical health violations are buried in government databases
- **Uninformed Dining Decisions**: People can't easily assess food safety risks before visiting restaurants  
- **Scattered Safety Information**: Inspection data, violation codes, and corrective actions are not centralized

### Target Users (Personas)

#### 1. **Sarah - Health-Conscious Customer** 
- **Age**: 32, Marketing Manager
- **Values**: Food safety, family health
- **Goals**: Find restaurants with excellent safety records for family dining
- **Pain Points**: Can't easily access inspection histories, worried about food poisoning

#### 2. **Mike - Restaurant Owner**
- **Age**: 45, Small Business Owner  
- **Values**: Reputation, customer trust
- **Goals**: Showcase excellent safety practices, improve visibility
- **Pain Points**: Potential customers don't see safety improvements, negative reviews overshadow safety efforts

#### 3. **Lisa - Health Inspector**
- **Age**: 38, City Health Department
- **Values**: Public health, regulatory compliance
- **Goals**: Ensure restaurants maintain safety standards, track improvement
- **Pain Points**: Limited public visibility of inspection data, hard to track trends

### Vision Statement
**"To create a transparent ecosystem where food safety information is accessible, empowering customers to make informed dining decisions while helping restaurants showcase their commitment to health standards."**

### Key Features / Goals
1. **Comprehensive Inspection History** - Complete timeline of all inspections with violation details
2. **Real-time Safety Scores** - 0-100 safety ratings based on latest inspections  
3. **Violation Transparency** - Detailed FDA violation codes with corrective actions
4. **Inspector Credibility** - Health inspector profiles with credentials and experience
5. **Restaurant Discovery** - Advanced filtering by safety scores, cuisine, location
6. **Admin Approval Workflow** - Quality control for restaurant listings
7. **Mobile-Responsive Design** - Accessible on all devices

### Success Metrics
- **User Engagement**: 80%+ of users check inspection history before restaurant visits
- **Data Accuracy**: 95%+ accuracy in safety score calculations
- **Restaurant Adoption**: 500+ restaurants onboarded in first 6 months  
- **Customer Trust**: 4.5+ star average app rating
- **Health Impact**: 20% reduction in food poisoning reports in coverage areas

### Assumptions & Constraints
**Assumptions:**
- Health department inspection data is publicly available
- Restaurants will voluntarily participate for transparency benefits
- Customers value safety information when choosing restaurants
- Mobile-first usage patterns for restaurant discovery

**Constraints:**
- Limited to publicly available inspection data
- Dependent on health department data accuracy and timeliness
- Must comply with data privacy and health information regulations
- Initial MVP budget of $50,000 for development and infrastructure

## 🚀 Quick Start - Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- Docker Desktop
- Git

### Docker Development (Recommended)
```bash
git clone [your-repo-url]
cd safebite
docker-compose up --build
```

**Access:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup
```bash
# Database setup
python create_database_from_csv.py

# Backend (Terminal 1)
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)  
cd frontend
npm install
npm run dev
```

## 🏗️ Architecture

SafeBite follows a modern web architecture with clear separation of concerns:

**Frontend (React)** → **Backend (FastAPI)** → **Database (SQLite)** → **Deployment (Docker)**

Data flows from CSV source files → SQLite database → FastAPI endpoints → React components → User interface

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS
- **Routing**: React Router v6
- **HTTP Client**: Axios
- **State Management**: React Context API

### Backend  
- **Framework**: FastAPI (Python 3.12)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with bcrypt
- **Validation**: Pydantic schemas
- **Server**: Uvicorn ASGI

### DevOps
- **Containerization**: Docker & Docker Compose
- **Database**: CSV-based data seeding
- **Development**: Hot reload for both frontend/backend

## 📂 Project Structure

```
safebite/
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components  
│   │   ├── services/        # API integration
│   │   └── context/         # Authentication context
│   ├── Dockerfile
│   └── package.json
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & database
│   │   ├── models/         # SQLAlchemy models
│   │   └── schemas/        # Pydantic schemas
│   ├── Dockerfile
│   └── requirements.txt
├── data/                    # CSV source files (single source of truth)
│   ├── restaurants.csv
│   ├── inspections.csv
│   ├── violations.csv
│   └── inspectors.csv
├── database/               # Generated SQLite database
├── docs/                   # Documentation
├── docker-compose.yml      # Multi-container setup
└── README.md
```

## 🔄 Branching Strategy (GitHub Flow)

We follow **GitHub Flow** for simple, continuous deployment:

1. **main** branch - Production-ready code
2. **feature/[feature-name]** - Feature development branches
3. **bugfix/[bug-description]** - Bug fix branches

### Workflow:
```bash
# Create feature branch
git checkout -b feature/inspection-timeline
git push -u origin feature/inspection-timeline

# Make changes, commit, push
git add .
git commit -m "Add inspection timeline component"
git push origin feature/inspection-timeline

# Create Pull Request → Review → Merge to main
```

## 🧪 Demo Accounts

- **Admin**: admin@safebite.demo / password123
- **Customer**: customer@safebite.demo / password123  
- **Restaurant Owner**: owner1@safebite.demo / password123

## 📖 Documentation

- [Complete Project Guide](CENTRALIZED_PROJECT_GUIDE.md) - Detailed technical documentation
- [API Documentation](docs/API_DOCUMENTATION.md) - REST API reference
- [Deployment Guide](docs/DEPLOYMENT_GUIDE.md) - Production deployment

## 🐳 Local Development Tools

### Required Tools
- **Docker Desktop**: Container orchestration
- **Visual Studio Code**: Primary IDE with extensions:
  - Docker Extension
  - Python Extension  
  - ES7+ React/Redux/React-Native snippets
  - Tailwind CSS IntelliSense
- **Postman/Insomnia**: API testing
- **Git**: Version control

### Development Workflow
1. Clone repository
2. Run `docker-compose up --build` for full stack
3. Make changes with hot reload enabled
4. Test endpoints via Swagger UI (localhost:8000/docs)
5. Commit to feature branch and create PR

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**SafeBite** - *Making food safety transparent, one inspection at a time.* 🛡️🍽️