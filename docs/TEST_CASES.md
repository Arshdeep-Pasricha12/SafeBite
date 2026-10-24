# SafeBite — Test Cases Catalog & Traceability Matrix

**Version:** 1.0.0  
**Test Suite Total:** 23 Tests + 7 Mutation Tests  
**Execution Status:** 100% Passed (All Green)  

---

## 1. Test Cases Master Table

| Test Case ID | Test Suite | Purpose / Scope | Input Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| **TC-AUTH-01** | `test_api.py` | Verify full user registration and JWT authentication | New user email, password, full name | 200 OK, valid JWT token issued | 200 OK, token issued | **PASSED** |
| **TC-DISC-01** | `test_api.py` | Verify restaurant approval and public discovery | Pending restaurant submission, admin approval | Restaurant appears in search results | Restaurant discovered | **PASSED** |
| **TC-ENG-01** | `test_assessment.py` | Clean inspection evaluates to maximum score | Inspection with 0 violations | Score: 100, Grade: "Excellent" | Score: 100, Grade: "Excellent" | **PASSED** |
| **TC-ENG-02** | `test_assessment.py` | Critical violation point penalty deduction | 1 Critical violation (-15 pts) | Score: 85, Deduction listed | Score: 85, Listed in factors | **PASSED** |
| **TC-ENG-03** | `test_assessment.py` | Expired/stale inspection penalties | Inspection > 365 days ago | Score penalized (-10 pts), warning active | Score: 90, Warning generated | **PASSED** |
| **TC-ENG-04** | `test_assessment.py` | Escalating repeat violation multiplier | 1 Critical violation with `is_repeat=True` | $1.5\times$ penalty (-22.5 pts) | Penalty -22.5 pts applied | **PASSED** |
| **TC-ENG-05** | `test_assessment.py` | Stale inspection warning flag generation | Inspection 400 days old | `data_freshness_status = "Stale"` | Status = "Stale" | **PASSED** |
| **TC-ENG-06** | `test_assessment.py` | Suspended license safety override | Restaurant with `license_status="Suspended"` | Score capped at $\le 35$, Grade: "High Risk" | Score: 35, Grade: "High Risk" | **PASSED** |
| **TC-ENG-07** | `test_assessment.py` | Synthetic record disclaimer generation | Restaurant with `is_synthetic=True` | Provenance disclaimer populated | Disclaimer text generated | **PASSED** |
| **TC-ENG-08** | `test_assessment.py` | Uninspected restaurant fallback handling | Restaurant with 0 inspection records | Score: 50, "Needs Inspection" | Score: 50, Status generated | **PASSED** |
| **TC-ENG-09** | `test_assessment.py` | Verified customer complaint deduction | 1 Verified health complaint | Score penalized (-5 pts) | Score penalized (-5 pts) | **PASSED** |
| **TC-CORR-01** | `test_disputes_and_admin.py` | Owner submits correction request & admin reviews | Correction payload with evidence URL | 201 Created, Admin reviews to 'Approved' | Status updated to 'Approved' | **PASSED** |
| **TC-MATCH-01** | `test_extension_and_matching.py` | Exact restaurant name match returns assessment | `name="Haldiram's Sweets & Restaurant"`, `city="Delhi"` | Matched: true, confidence $\ge 0.90$, assessment included | Matched: true, confidence 1.0 | **PASSED** |
| **TC-MATCH-02** | `test_extension_and_matching.py` | Fuzzy restaurant name match | `name="Chipotle Grill"`, `city="New York"` | Matched: true, confidence $\ge 0.70$ | Matched: true, confidence 0.85 | **PASSED** |
| **TC-MATCH-03** | `test_extension_and_matching.py` | POST variant matching endpoint | JSON body with name, city, platform | Matched: true, response JSON valid | 200 OK, matched | **PASSED** |
| **TC-MATCH-04** | `test_extension_and_matching.py` | Unmatched restaurant returns graceful response | `name="NonExistentBakery12345XYZ"` | Matched: false, confidence 0.0, no error | 200 OK, matched: false | **PASSED** |
| **TC-PROV-01** | `test_provenance.py` | Restaurant API returns complete provenance fields | `GET /api/restaurants/R0001` | Payload includes `source_name`, `source_url`, `is_synthetic` | All provenance fields present | **PASSED** |
| **TC-PROV-02** | `test_provenance.py` | Synthetic benchmark records are explicitly tagged | Query benchmark records | `is_synthetic == True` for all 1000 fixtures | 1000/1000 tagged synthetic | **PASSED** |
| **TC-PROV-03** | `test_provenance.py` | Verified official records marked non-synthetic | Query FSSAI / NYC records | `is_synthetic == False`, `status == "Verified Official"` | Ingested records verified | **PASSED** |
| **TC-REG-01** | `test_regression.py` | Admin login succeeds without KeyError (bcrypt fix) | `admin@safebite.demo` / `adminpassword` | 200 OK, JWT access token returned | 200 OK, token returned | **PASSED** |
| **TC-REG-02** | `test_regression.py` | Customer login succeeds with seeded credentials | `customer@safebite.demo` / `password123` | 200 OK, JWT access token returned | 200 OK, token returned | **PASSED** |
| **TC-REG-03** | `test_regression.py` | Database URL resolution not hardcoded to D: drive | Environment inspection of `config.DATABASE_URL` | Resolves dynamically without `d:/` prefix | Path resolves dynamically | **PASSED** |
| **TC-REG-04** | `test_regression.py` | Profile alias route `/api/profile` returns session | Bearer JWT header on `GET /api/profile` | 200 OK, user profile JSON returned | 200 OK, profile returned | **PASSED** |

---

## 2. Mutation Testing Catalog

| Mutant ID | Targeted Logic in `assessment.py` | Injected Fault | Test Catching Mutant | Kill Status |
|---|---|---|---|---|
| **MUT-01** | Clean Inspection Base Score | Changed base score from 100 to 90 | `TC-ENG-01` | **KILLED** |
| **MUT-02** | Critical Violation Penalty | Reduced critical deduction from -15 to -5 | `TC-ENG-02` | **KILLED** |
| **MUT-03** | Repeat Multiplier | Inverted repeat multiplier from 1.5 to 1.0 | `TC-ENG-04` | **KILLED** |
| **MUT-04** | Staleness Deduction | Set staleness deduction to 0 (no penalty) | `TC-ENG-03` | **KILLED** |
| **MUT-05** | License Suspension Cap | Raised suspended license score cap to 60 | `TC-ENG-06` | **KILLED** |
| **MUT-06** | Uninspected Fallback | Changed fallback score from 50 to 80 | `TC-ENG-08` | **KILLED** |
| **MUT-07** | Complaint Penalty | Removed complaint deduction logic | `TC-ENG-09` | **KILLED** |

**Summary:** 7 Mutants Generated, 7 Mutants Killed. **Mutation Score: 100%**.
