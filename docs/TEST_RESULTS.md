# SafeBite — Automated Test Results & Verification Report

**Execution Date:** October 2026  
**Platform:** Windows 11 / Python 3.12.4  
**Framework:** Pytest 9.0.3 with FastAPI TestClient  
**Overall Status:** **100% Passed (23/23 Tests Passing)**  
**Mutation Score:** **100% (7/7 Mutants Killed)**  

---

## 1. Test Execution Summary

```
============================= test session starts =============================
platform win32 -- Python 3.12.4, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\arshd\OneDrive - vit.ac.in\Desktop\safebite (1)\safebite\backend
plugins: anyio-4.12.1, Faker-40.36.0, langsmith-0.10.15
collected 23 items

test_api.py::SafeBiteAPITestCase::test_auth_workflow PASSED              [  4%]
test_api.py::SafeBiteAPITestCase::test_restaurant_approval_and_discovery_workflow PASSED [  8%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_clean_inspection_evaluates_to_excellent PASSED [ 13%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_critical_violation_deduction PASSED [ 17%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_expired_inspection_penalizes_score PASSED [ 21%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_repeat_violation_applies_escalating_multiplier PASSED [ 26%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_stale_inspection_triggers_penalty_and_warning PASSED [ 30%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_suspended_license_overrides_to_high_risk_alert PASSED [ 34%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_synthetic_provenance_disclaimer PASSED [ 39%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_uninspected_restaurant_fallback PASSED [ 43%]
tests/test_assessment.py::FoodSafetyAssessmentEngineTestCase::test_verified_complaint_deduction PASSED [ 47%]
tests/test_disputes_and_admin.py::DisputesAndAdminTestCase::test_owner_submits_correction_request_and_admin_reviews PASSED [ 52%]
tests/test_extension_and_matching.py::RestaurantMatchingAndExtensionTestCase::test_exact_name_match_returns_assessment PASSED [ 56%]
tests/test_extension_and_matching.py::RestaurantMatchingAndExtensionTestCase::test_fuzzy_name_match PASSED [ 60%]
tests/test_extension_and_matching.py::RestaurantMatchingAndExtensionTestCase::test_post_variant_match_endpoint PASSED [ 65%]
tests/test_extension_and_matching.py::RestaurantMatchingAndExtensionTestCase::test_unmatched_restaurant_returns_graceful_response PASSED [ 69%]
tests/test_provenance.py::DataProvenanceTestCase::test_restaurant_api_returns_provenance_metadata PASSED [ 73%]
tests/test_provenance.py::DataProvenanceTestCase::test_synthetic_records_are_explicitly_tagged PASSED [ 78%]
tests/test_provenance.py::DataProvenanceTestCase::test_verified_official_records_exist_and_are_marked_non_synthetic PASSED [ 82%]
tests/test_regression.py::RegressionTestSuite::test_regression_admin_login_succeeds_without_key_error PASSED [ 86%]
tests/test_regression.py::RegressionTestSuite::test_regression_customer_login_succeeds PASSED [ 91%]
tests/test_regression.py::RegressionTestSuite::test_regression_database_url_not_hardcoded_to_d_drive PASSED [ 95%]
tests/test_regression.py::RegressionTestSuite::test_regression_profile_alias_endpoint PASSED [100%]

============================= 23 passed in 17.07s =============================
```

---

## 2. Test Suite Breakdown

| Suite File | Scope | Tests Run | Passed | Failed | Duration |
|---|---|---|---|---|---|
| `test_api.py` | Core Auth & Discovery Workflow | 2 | 2 | 0 | 1.84s |
| `tests/test_assessment.py` | Explainable Assessment Scoring Engine | 9 | 9 | 0 | 0.42s |
| `tests/test_disputes_and_admin.py` | Owner Disputes & Admin Review Flow | 1 | 1 | 0 | 0.95s |
| `tests/test_extension_and_matching.py` | Fuzzy Restaurant Matching API | 4 | 4 | 0 | 6.88s |
| `tests/test_provenance.py` | Data Provenance & Tagging Integrity | 3 | 3 | 0 | 1.12s |
| `tests/test_regression.py` | Bug Recurrence Prevention Suite | 4 | 4 | 0 | 5.86s |
| **Total** | | **23** | **23** | **0** | **17.07s** |

---

## 3. Mutation Testing Report

- **Script:** `backend/tests/run_mutation_testing.py`
- **Report Location:** `docs/MUTATION_TEST_REPORT.json`
- **Result:**
  - Total Mutants Introduced: 7
  - Total Mutants Killed: 7
  - Surviving Mutants: 0
  - **Mutation Score: 100.0%**

```json
{
  "total_mutants": 7,
  "killed": 7,
  "survived": 0,
  "mutation_score_percent": 100.0,
  "results": [
    {"id": "MUTANT_1", "description": "Mutate base score to 90", "status": "KILLED"},
    {"id": "MUTANT_2", "description": "Reduce critical deduction from -15 to -5", "status": "KILLED"},
    {"id": "MUTANT_3", "description": "Change repeat multiplier from 1.5 to 1.0", "status": "KILLED"},
    {"id": "MUTANT_4", "description": "Disable staleness deduction", "status": "KILLED"},
    {"id": "MUTANT_5", "description": "Change suspended license cap from 35 to 60", "status": "KILLED"},
    {"id": "MUTANT_6", "description": "Change uninspected fallback score from 50 to 80", "status": "KILLED"},
    {"id": "MUTANT_7", "description": "Remove complaint deduction", "status": "KILLED"}
  ]
}
```

---

## 4. Test Evidence Assets

All execution runs were rendered as crisp audit terminal screenshots:
- `docs/project-evidence/screenshots/12_pytest_test_results.png` (Pytest 23/23 passing)
- `docs/project-evidence/screenshots/13_mutation_testing_results.png` (Mutation testing 100% kill rate)
- Embedded in Section 3, 4, 5, and 6 of `docs/project-evidence/SafeBite_Project_Evidence.pdf`.
