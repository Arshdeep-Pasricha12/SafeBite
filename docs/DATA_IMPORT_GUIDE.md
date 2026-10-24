# SafeBite — Data Import & Ingestion Pipeline Guide

**Pipeline Version:** 1.0.0  
**Utility Script:** `backend/ingest_inspection_data.py`  

---

## 1. Overview

The SafeBite data import pipeline standardizes external inspection datasets into the relational database. It ensures that only properly validated, structured, and attributed data is ingested into `database/safebite.db`, while recording data provenance and handling malformed entries safely.

---

## 2. Ingestion CLI Tool

The pipeline is executed from the terminal using Python:

```bash
cd backend
python ingest_inspection_data.py --file data/verified_inspection_records.json
```

### CLI Options:
- `--file <path>`: Path to JSON inspection payload file (defaults to `data/verified_inspection_records.json`).
- `--dry-run`: Validates payload schema and records without writing to the database.
- `--verbose`: Prints detailed per-record field mapping logs.

---

## 3. Ingestion Payload Schema (JSON)

Input files must adhere to the standardized SafeBite inspection structure:

```json
[
  {
    "restaurant": {
      "id": "R0001",
      "name": "Haldiram's Sweets & Restaurant",
      "cuisine": "North Indian, Sweets",
      "address": "Connaught Place, Block L",
      "city": "Delhi",
      "state": "Delhi",
      "postal_code": "110001",
      "phone": "+91-11-41512345",
      "license_number": "10014011001234",
      "license_status": "Active",
      "source_name": "FSSAI FoSTaC Registry",
      "source_url": "https://fostac.fssai.gov.in/records/10014011001234",
      "source_record_id": "FSSAI-DEL-2024-001234",
      "verification_status": "Verified Official",
      "confidence_score": 0.98,
      "is_synthetic": false
    },
    "inspection": {
      "id": "INSP0001",
      "inspection_date": "2024-09-15T10:30:00Z",
      "score": 96,
      "result": "Passed",
      "inspector_id": "INS001",
      "source_name": "FSSAI Food Safety Audit",
      "source_url": "https://fostac.fssai.gov.in/audits/INSP0001",
      "is_synthetic": false,
      "data_freshness_status": "Fresh"
    },
    "violations": [
      {
        "code": "FSSAI-04-A",
        "description": "Minor water temperature deviation in secondary handwash sink",
        "severity": "Minor",
        "is_critical": false,
        "is_repeat": false,
        "status": "Corrected On Site"
      }
    ]
  }
]
```

---

## 4. Ingestion Validation Rules

Before an inspection row is committed to the database, the pipeline validates:
1. **Restaurant License Integrity:** Validates that `license_number` is populated and matches country formatting standards.
2. **Date Boundaries:** Rejects inspections dated in the future or older than 5 years without historical archive flags.
3. **Score Boundaries:** Validates that `score` is an integer between 0 and 100.
4. **Violation Referential Integrity:** Ensures violation codes map to known classifications or generates automatic fallback categorization.
5. **Deduplication:** Prevents duplicate insertions by checking `(restaurant_id, inspection_date, source_record_id)`.

---

## 5. Rejected Record Handling

When invalid rows are encountered during import:
- The error is logged with the row index, field name, and rejection reason.
- The rejected record is appended to `backend/data/rejected_imports.log`.
- Valid rows within the batch proceed without aborting the entire ingestion process (transactional batching per restaurant).

---

## 6. Database Schema Migration

Before running an ingestion on a fresh database, execute:
```bash
cd backend
python migrate_db.py
```
This adds all required provenance columns and creates the `correction_requests` table if not already present.
