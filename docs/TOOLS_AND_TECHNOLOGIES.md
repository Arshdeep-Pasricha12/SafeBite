# SafeBite — Tools & Technologies Inventory

**Document Version:** 1.0.0  
**Audit Scope:** Active, Verifiable Dependencies Only  

---

## 1. Inventory Summary

This document catalogues only the technologies, libraries, and frameworks actively utilized in the finalized SafeBite codebase. No theoretical or unintegrated tools are listed.

---

## 2. Comprehensive Technology Catalog

| Layer | Technology | Version | Location / Usage | Purpose | Local Executable? | Requires Credentials? | Implementation Status |
|---|---|---|---|---|---|---|---|
| **Backend Core** | Python | 3.12.4 | System runtime | Primary programming language | Yes | No | **Fully Implemented** |
| **Backend Core** | FastAPI | 0.100+ | `backend/app/main.py` | High-performance asynchronous REST API framework | Yes | No | **Fully Implemented** |
| **Backend Core** | Uvicorn | 0.40.0 | `backend` server | Lightning-fast ASGI web server implementation | Yes | No | **Fully Implemented** |
| **Backend Core** | Pydantic v2 | 2.12.5 | `backend/app/schemas/` | Request/response data validation and settings management | Yes | No | **Fully Implemented** |
| **Database & ORM**| SQLAlchemy | 2.0.51 | `backend/app/core/database.py` | Declarative object-relational mapping and connection pooling | Yes | No | **Fully Implemented** |
| **Database & ORM**| SQLite | 3.x | `database/safebite.db` | Embedded relational database engine for zero-config portability | Yes | No | **Fully Implemented** |
| **Security & Auth**| Passlib (Bcrypt)| 1.7.4 | `backend/app/core/security.py` | Password hashing with salt generation and timing-attack protection | Yes | No | **Fully Implemented** |
| **Security & Auth**| PyJWT | 2.13.0 | `backend/app/core/security.py` | Cryptographically signed JSON Web Token creation & verification | Yes | No | **Fully Implemented** |
| **Assessment** | RapidFuzz / Custom | 3.14.5 | `backend/app/api/restaurants.py`| Levenshtein distance fuzzy string matching for restaurant queries | Yes | No | **Fully Implemented** |
| **Frontend Core** | React | 18.2.0 | `frontend/src/` | Component-based single-page reactive application framework | Yes | No | **Fully Implemented** |
| **Frontend Core** | Vite | 4.5.14 | `frontend/vite.config.js` | Modern frontend bundling, fast HMR, and build optimization | Yes | No | **Fully Implemented** |
| **Frontend Core** | React Router DOM| 6.15.0| `frontend/src/App.jsx` | Client-side declarative routing and protected route guards | Yes | No | **Fully Implemented** |
| **Frontend Styling**| Tailwind CSS | 3.3.3 | `frontend/tailwind.config.js` | Utility-first responsive CSS styling with custom design tokens | Yes | No | **Fully Implemented** |
| **Frontend Styling**| Lucide React | 0.268.0| `frontend/src/components/` | Consistent SVG icon library for UI controls and safety shields | Yes | No | **Fully Implemented** |
| **Frontend HTTP** | Axios | 1.5.0 | `frontend/src/services/api.js` | HTTP client with automatic JWT bearer authorization interceptors | Yes | No | **Fully Implemented** |
| **Browser Ext** | Manifest V3 | 3.0 | `extension/` | Chrome browser extension with service worker and content script | Yes | No | **Fully Implemented** |
| **Test Automation**| Pytest | 9.0.3 | `backend/tests/` | Automated unit, integration, and regression testing framework | Yes | No | **Fully Implemented** |
| **Test Automation**| FastAPI TestClient| (Starlette) | `backend/tests/` | In-memory HTTP client testing API endpoints without network port binding | Yes | No | **Fully Implemented** |
| **Mutation Testing**| Custom AST Runner| 1.0.0 | `backend/tests/run_mutation_testing.py` | Systematic fault-injection framework testing scoring resilience | Yes | No | **Fully Implemented** |
| **Browser Auto** | Selenium WebDriver| 4.45.0 | `backend/capture_all_evidence.py`| Headless Chrome browser automation for capturing genuine screenshots | Yes | No | **Fully Implemented** |
| **Evidence Report**| ReportLab | 5.0.1 | `backend/generate_consolidated_pdf.py`| Programmatic generation of the consolidated multi-page PDF dossier | Yes | No | **Fully Implemented** |
| **Image Processing**| Pillow (PIL) | 11.2.1 | `backend/generate_consolidated_pdf.py`| Image aspect-ratio scaling, dimension checking, and terminal rendering | Yes | No | **Fully Implemented** |
| **Containerization**| Docker Compose | 3.8 | `docker-compose.yml` | Multi-container specification linking FastAPI backend and React Vite SPA | Yes | No | **Fully Implemented** |
| **Version Control**| Git | 2.x | Root repository | Distributed version control with branching and commit hygiene | Yes | No | **Fully Implemented** |

---

## 3. Deliberately Bounded Integrations

- **Commercial Food Delivery APIs (Swiggy, Zomato):** Requires enterprise partnership contracts and private API gateways; handled via the Manifest V3 Chrome Extension and the Companion Ordering Demonstration.
- **FSSAI Real-Time Push Webhooks:** FSSAI public portals do not offer webhook callbacks; handled via batch JSON ingestion (`ingest_inspection_data.py`).
