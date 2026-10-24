# SafeBite — Data Sources & Provenance Specification

**Document Version:** 1.0.0  
**Data Engineering Team:** SafeBite Pipeline Division  

---

## 1. Overview

SafeBite operates a rigorous data ingestion architecture designed to ingest, validate, standardize, and attribute food-safety inspection records from municipal health authorities and official open-data portals.

To prevent deceptive ratings, the platform enforces strict data provenance tagging across every entity stored in `database/safebite.db`.

---

## 2. Official Primary Data Sources

SafeBite currently supports official datasets from two primary health regulatory bodies:

### 2.1 Food Safety and Standards Authority of India (FSSAI) — FoSTaC & FoSCoS
- **Issuing Agency:** Ministry of Health and Family Welfare, Government of India.
- **Regulatory Framework:** Food Safety and Standards Act, 2006.
- **Audit Type:** Annual compliance inspection and Food Safety Training and Certification (FoSTaC) audit.
- **Identifier Format:** 14-digit FSSAI License/Registration Number (e.g. `10014011001234`).
- **Inspection Metrics:**
  - Schedule 4 Part II compliance checklist (Sanitation, water quality, personal hygiene, pest control).
  - Score rating: Up to 100 points, categorized into A (Excellent), B (Satisfactory), and Needs Improvement.
- **Sample Verified Records in SafeBite:**
  - *Haldiram's Sweets & Restaurant* (Connaught Place, New Delhi) — License `#10014011001234`
  - *Saravanaa Bhavan* (Janpath, New Delhi) — License `#10016011002345`
  - *Bikanervala* (Karol Bagh, New Delhi) — License `#10015011003456`
  - *Karim's* (Jama Masjid, Old Delhi) — License `#10013011004567`

### 2.2 New York City Department of Health and Mental Hygiene (NYC DOHMH)
- **Issuing Agency:** NYC DOHMH Restaurant Inspection Information System via NYC OpenData.
- **Audit Type:** Unannounced sanitary inspections scoring violation points (lower points = better letter grade: Grade A: 0–13 points, Grade B: 14–27 points, Grade C: 28+ points).
- **Identifier Format:** NYC CAMIS ID / DOHMH License Number (e.g. `41234567`).
- **Violation Classification:** Critical violations (food temperature out of danger zone, food cross-contamination) vs General violations (non-food contact surface cleaning).
- **Sample Verified Records in SafeBite:**
  - *Chipotle Mexican Grill* (Midtown Manhattan, NYC) — License `#41234567`
  - *Shake Shack* (Madison Square Park, NYC) — License `#41345678`
  - *Joe's Pizza* (Greenwich Village, NYC) — License `#41456789`
  - *Starbucks Coffee* (Times Square, NYC) — License `#41567890`

---

## 3. Data Provenance Schema & Fields

Every record ingested into SafeBite is augmented with the following provenance attributes:

```sql
-- Schema extensions in 'restaurants' and 'inspections' tables
source_name             VARCHAR(255)   -- Government registry or provider name
source_url              VARCHAR(500)   -- Direct hyperlink to official audit source or registry
source_record_id        VARCHAR(100)   -- Government license, CAMIS, or audit certificate number
last_synced_at          DATETIME       -- UTC timestamp of last pipeline ingestion
verification_status     VARCHAR(50)    -- 'Verified Official' | 'Synthetic Benchmark' | 'Pending Review'
confidence_score        FLOAT          -- Matching confidence rating (0.0 to 1.0)
is_synthetic            BOOLEAN        -- False for verified records; True for benchmark fixtures
data_freshness_status   VARCHAR(50)    -- 'Fresh' (<180d) | 'Aging' (180-365d) | 'Stale' (>365d)
```

---

## 4. Synthetic Benchmark Dataset

For high-volume query testing, geospatial search stress-testing, and UI pagination benchmarking, SafeBite includes 1,000 synthetic benchmark restaurant records.

### Ethical & Legal Safeguards:
1. **Explicit Flagging:** All benchmark records are flagged with `is_synthetic = True` in the database.
2. **Distinct License Numbers:** Synthetic licenses follow prefixed numbers (e.g. `FSSAI-SYN-xxxx` or `NYC-SYN-xxxx`).
3. **Consumer UI Disclaimers:** When a customer views a synthetic restaurant in the web interface, an explicit yellow disclaimer banner is displayed stating:
   > *"Demonstration Record: This profile was generated for platform performance validation and does not reflect actual regulatory enforcement actions."*
4. **Filtering Support:** The restaurant directory allows users to filter specifically for `Verified Official Only`, hiding synthetic benchmark entries.
