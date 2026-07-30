# SafeBite Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           SAFEBITE ARCHITECTURE                                │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐
│   FRONTEND      │    │    BACKEND      │    │   DATABASE      │    │ DEPLOYMENT  │
│                 │    │                 │    │                 │    │             │
│  React 18       │───▶│  FastAPI        │───▶│  SQLite         │───▶│ Docker      │
│  Vite           │    │  Python 3.12    │    │  SQLAlchemy ORM │    │ Compose     │
│  Tailwind CSS   │    │  Uvicorn ASGI   │    │                 │    │             │
│  Axios          │    │  JWT Auth       │    │                 │    │             │
│                 │    │  Pydantic       │    │                 │    │             │
│  Port: 3001     │    │  Port: 8000     │    │  File-based     │    │ Multi-stage │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────┘
         │                       │                       │                    │
         │                       │                       │                    │
         ▼                       ▼                       ▼                    ▼

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────┐
│   USER FLOWS    │    │   API LAYER     │    │   DATA FLOW     │    │  SERVICES   │
│                 │    │                 │    │                 │    │             │
│ • Browse        │    │ • /restaurants  │    │ CSV Files       │    │ • Frontend  │
│ • Search        │    │ • /auth         │    │      ↓          │    │   Container │
│ • Filter        │    │ • /inspections  │    │ Database        │    │ • Backend   │
│ • View Details  │    │ • /admin        │    │      ↓          │    │   Container │
│ • Inspect       │    │ • OpenAPI       │    │ API Endpoints   │    │ • Database  │
│ • Manage        │    │ • JWT Security  │    │      ↓          │    │   Setup     │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────┘

                              DATA FLOW LEGEND
┌─────────────────────────────────────────────────────────────────────────────────┐
│  ───▶  HTTP Requests/Responses    │    📊  Data Source           │               │
│  ═══▶  Database Queries           │    🔐  Authentication        │               │  
│  ╋━━▶  Docker Communication       │    🌐  Web Interface         │               │
│  ┄┄▶   Configuration Flow         │    📱  Mobile Responsive     │               │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Detailed Component Breakdown

### Frontend Layer (Port 3001)
- **Framework**: React 18 with modern hooks
- **Build Tool**: Vite for fast development and building
- **Styling**: Tailwind CSS for responsive design
- **Routing**: React Router v6 for SPA navigation
- **State**: React Context API for authentication
- **HTTP Client**: Axios for API communication
- **Key Features**: 
  - Mobile-responsive design
  - Real-time data updates
  - Progressive loading states
  - Component-based architecture

### Backend Layer (Port 8000)
- **Framework**: FastAPI for high-performance async API
- **Runtime**: Python 3.12 with type hints
- **Server**: Uvicorn ASGI for production-ready serving
- **Authentication**: JWT tokens with bcrypt hashing
- **Validation**: Pydantic schemas for request/response
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Key Features**:
  - Role-based access control (Customer/Owner/Admin)
  - Comprehensive inspection history API
  - Real-time safety score calculations
  - RESTful API design

### Database Layer
- **Primary**: SQLite for development (PostgreSQL-ready)
- **ORM**: SQLAlchemy for object-relational mapping
- **Data Source**: CSV files as single source of truth
- **Key Tables**: 
  - Users (authentication & roles)
  - Restaurants (business information)
  - Inspections (health department records)
  - Violations (safety infractions)
  - Inspectors (health official credentials)

### Deployment Layer
- **Containerization**: Docker & Docker Compose
- **Services**: Multi-container setup with networking
- **Development**: Hot reload for both frontend/backend
- **Production Ready**: Environment-based configuration
- **Scalability**: Horizontal scaling support

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                           │
├─────────────────────────────────────────────────────────────────┤
│  🔐 JWT Authentication    │  Input Validation                   │
│  🛡️  Role-Based Access    │  CORS Protection                    │
│  🔒 Password Hashing      │  HTTPS Ready                        │
│  🚪 Protected Routes      │  SQL Injection Prevention           │
└─────────────────────────────────────────────────────────────────┘
```

## API Architecture

### Core Endpoints
```
/api/auth/*           - Authentication & user management
/api/restaurants/*    - Restaurant CRUD & discovery
/api/inspections/*    - Inspection history & violations
/api/admin/*          - Administrative functions
```

### Authentication Flow
```
User Login ──▶ JWT Token ──▶ Protected API ──▶ Role Validation ──▶ Resource Access
```

## Data Architecture

### CSV to Database Pipeline
```
CSV Files ──▶ Validation ──▶ SQLite ──▶ SQLAlchemy Models ──▶ FastAPI ──▶ React UI
```

### Real-time Updates
```
User Action ──▶ API Request ──▶ Database Update ──▶ Response ──▶ UI Refresh
```

## Development Workflow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  LOCAL DEV      │    │   TESTING       │    │   DEPLOYMENT    │
│                 │    │                 │    │                 │
│ • Hot Reload    │───▶│ • API Testing   │───▶│ • Docker Build  │
│ • Live Backend  │    │ • UI Testing    │    │ • Multi-stage   │
│ • Database      │    │ • Integration   │    │ • Production    │
│   Seeding       │    │   Testing       │    │   Ready         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Performance Considerations

- **Frontend**: Code splitting, lazy loading, optimized images
- **Backend**: Async operations, efficient queries, caching strategies
- **Database**: Indexed queries, optimized relationships
- **Docker**: Multi-stage builds, layer caching

This architecture supports the core SafeBite mission of food safety transparency while maintaining scalability, security, and developer productivity.