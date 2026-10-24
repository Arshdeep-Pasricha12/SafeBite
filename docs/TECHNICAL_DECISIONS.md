# SafeBite — Technical Decisions & Architecture Rationale

**Document Version:** 1.0.0  
**Author:** SafeBite Engineering Architecture Committee  

---

## 1. Overview

This document formalizes the architectural decisions, design patterns, and engineering trade-offs adopted across the SafeBite platform to ensure stability, transparency, explainability, and maintainability.

---

## 2. Assessment Engine & Scoring Policy

### Decision: Deterministic, Explainable Formula over Opaque Machine Learning
- **Context:** An opaque machine-learning model (such as a black-box neural net) would make it impossible for restaurant owners and health inspectors to understand why a safety score was downgraded, raising legal and fairness concerns.
- **Decision:** Implemented a rule-based deterministic scoring engine (`FoodSafetyAssessmentEngine` in `backend/app/core/assessment.py`) governed by clear mathematical rules:
  $$\text{Safety Score} = \max\left(0, \min\left(100, 100 - \sum \text{Deductions}\right)\right)$$
- **Scoring Multipliers & Weights:**
  - **Base Score:** 100 points (clean inspection baseline).
  - **Critical Infractions:** -15 to -20 points per infraction (food adulteration, temperature violations, pest activity).
  - **Non-Critical Infractions:** -5 points per infraction (labeling, minor equipment wear).
  - **Repeat Violation Multiplier ($1.5\times$):** If an establishment repeats the same infraction in subsequent inspections, the penalty escalates by $1.5\times$ to reflect systematic operational neglect.
  - **Recency & Staleness ($>365$ days):** -10 points penalty plus prominent warning pill. If health records are outdated, consumers must not be given unjustified reassurance.
  - **License Suspension:** Overrides calculated score to $\le 35$ with a "High Risk / Immediate Alert" badge.

---

## 3. Data Provenance & Synthetic Data Handling

### Decision: Strict Segregation & Full Field Attribution
- **Context:** For testing, development, and stress benchmarking, repositories often contain thousands of generated fake records. If these are presented to consumers without disclaimers, the platform violates trust and risks liability.
- **Decision:**
  - Every restaurant and inspection record in `database/safebite.db` now carries explicit provenance metadata columns (`source_name`, `source_url`, `source_record_id`, `verification_status`, `is_synthetic`, `data_freshness_status`).
  - Records originating from government databases (FSSAI, NYC OpenData) are marked `is_synthetic = False` and `verification_status = "Verified Official"`.
  - The 1,000 stress benchmark fixtures are marked `is_synthetic = True` and `verification_status = "Synthetic Benchmark"`.
  - In the UI, synthetic records display an explicit disclaimer banner: *"Synthetic Demonstration Record: This record is generated for system validation and does not represent an actual health agency audit."*

---

## 4. Browser Extension Architecture (Manifest V3)

### Decision: Manifest V3 with Service Worker and Content Script Injection
- **Context:** Manifest V2 is deprecated by Google Chrome. Modern extensions must use Manifest V3, which mandates ephemeral service workers rather than persistent background pages.
- **Architecture:**
  - `manifest.json`: Declares `permissions: ["storage", "activeTab"]` and `host_permissions: ["http://127.0.0.1:8000/*", "http://localhost:8000/*"]`.
  - `background.js`: Service worker handling caching and asynchronous fetch requests to `GET /api/restaurants/match`.
  - `content.js`: Content script that scans restaurant titles in the active page DOM (e.g. `<h1>`, `.restaurant-name`), queries the background worker, and dynamically injects a floating, draggable SafeBite safety pill (`safebite-extension-pill`) and modal.
  - `popup.html` & `popup.js`: Quick lookup interface allowing users to manually search restaurant safety scores directly from their browser toolbar.

---

## 5. Companion Ordering Demo vs Commercial Injection

### Decision: Interactive Simulated Ordering Platform at `/demo/order`
- **Context:** Commercial delivery platforms (Swiggy, Zomato, DoorDash) do not offer public third-party injection APIs. Unauthorized reverse-engineering of live authenticated delivery apps violates Terms of Service, risks IP blocks, and creates brittle external dependencies during evaluation.
- **Decision:** Built a high-fidelity companion food delivery demonstration (`frontend/src/pages/CompanionOrderingDemo.jsx`).
  - Evaluators can select from real restaurants (e.g. *Haldiram's Sweets & Restaurant*, *Chipotle Mexican Grill*), browse dishes, add items to a delivery basket, and experience real-time SafeBite floating pill injection and pre-checkout food safety advisories.
  - Enables 100% reproducible, zero-credential evaluation that operates offline and locally without paying for food orders.

---

## 6. Database Portability: SQLite and PostgreSQL

### Decision: Dynamic Path Resolution with SQLAlchemy 2.0
- **Context:** Hardcoded absolute file paths (e.g. `d:/safebite`) break immediately when cloned to different drives, developer machines, or CI/CD pipelines.
- **Decision:**
  - Implemented dynamic path resolution in `backend/app/core/config.py` using `pathlib.Path(__file__).resolve()`.
  - Maintained full SQLAlchemy 2.0 ORM compatibility, enabling seamless transition to PostgreSQL in production environments simply by providing the `DATABASE_URL=postgresql://user:pass@host:5432/safebite` environment variable without altering application code.
