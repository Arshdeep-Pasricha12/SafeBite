import os
import sys
import json
import unittest
from io import StringIO
from typing import Dict, Any, List

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.assessment import FoodSafetyAssessmentEngine
import tests.test_assessment as test_assessment_module

MUTATIONS = [
    {
        "id": "MUT_01",
        "description": "Mutate CRITICAL_PENALTY: 18 -> 0 (ignore critical violations)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "CRITICAL_PENALTY", 0),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "CRITICAL_PENALTY", 18)
    },
    {
        "id": "MUT_02",
        "description": "Mutate CRITICAL_PENALTY: 18 -> 5 (insufficient penalty)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "CRITICAL_PENALTY", 5),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "CRITICAL_PENALTY", 18)
    },
    {
        "id": "MUT_03",
        "description": "Mutate REPEAT_MULTIPLIER: 1.5 -> 1.0 (no escalating penalty for repeats)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "REPEAT_MULTIPLIER", 1.0),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "REPEAT_MULTIPLIER", 1.5)
    },
    {
        "id": "MUT_04",
        "description": "Mutate VERIFIED_COMPLAINT_PENALTY: 6 -> 0 (ignore complaints)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "VERIFIED_COMPLAINT_PENALTY", 0),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "VERIFIED_COMPLAINT_PENALTY", 6)
    },
    {
        "id": "MUT_05",
        "description": "Mutate STALE_DAYS_THRESHOLD: 365 -> 9999 (never flag inspections as stale)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "STALE_DAYS_THRESHOLD", 9999),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "STALE_DAYS_THRESHOLD", 365)
    },
    {
        "id": "MUT_06",
        "description": "Mutate EXPIRED_DAYS_THRESHOLD: 730 -> 9999 (never expire old data)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "EXPIRED_DAYS_THRESHOLD", 9999),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "EXPIRED_DAYS_THRESHOLD", 730)
    },
    {
        "id": "MUT_07",
        "description": "Mutate REPEAT_MULTIPLIER: 1.5 -> 0.0 (zero penalty on repeats)",
        "apply": lambda: setattr(FoodSafetyAssessmentEngine, "REPEAT_MULTIPLIER", 0.0),
        "revert": lambda: setattr(FoodSafetyAssessmentEngine, "REPEAT_MULTIPLIER", 1.5)
    }
]

def run_mutation_tests():
    print("=" * 65)
    print("SafeBite Systematic Mutation Testing — Risk Assessment Engine")
    print("Target: backend/app/core/assessment.py")
    print("=" * 65)

    results = []
    killed_count = 0
    total_mutants = len(MUTATIONS)

    # 1. Baseline verification: ensure tests pass on unmutated code
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_assessment_module)
    runner = unittest.TextTestRunner(stream=StringIO(), verbosity=0)
    baseline_result = runner.run(suite)

    if not baseline_result.wasSuccessful():
        print("ERROR: Baseline tests failed on unmutated code! Fix unit tests first.")
        return False

    print("[OK] Baseline test suite passes (100% on pristine code).\n")

    # 2. Run mutations
    for m in MUTATIONS:
        m_id = m["id"]
        desc = m["description"]
        m["apply"]()

        # Run test suite against mutant
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_assessment_module)
        runner = unittest.TextTestRunner(stream=StringIO(), verbosity=0)
        test_res = runner.run(suite)

        m["revert"]()

        if not test_res.wasSuccessful():
            status = "KILLED"
            killed_count += 1
            print(f"[{m_id}] {status}: {desc}")
        else:
            status = "SURVIVED"
            print(f"[{m_id}] {status} (Warning! Test suite did not catch): {desc}")

        results.append({
            "id": m_id,
            "description": desc,
            "status": status,
            "failures": len(test_res.failures),
            "errors": len(test_res.errors)
        })

    mutation_score = (killed_count / total_mutants) * 100.0

    print("\n" + "=" * 65)
    print("Mutation Testing Summary:")
    print(f"  Total Mutants Generated: {total_mutants}")
    print(f"  Mutants Killed:          {killed_count}")
    print(f"  Mutants Survived:        {total_mutants - killed_count}")
    print(f"  Mutation Score:          {mutation_score:.1f}%")
    print("=" * 65)

    # Write report
    report_data = {
        "target": "backend/app/core/assessment.py",
        "total_mutants": total_mutants,
        "killed_mutants": killed_count,
        "survived_mutants": total_mutants - killed_count,
        "mutation_score_percent": mutation_score,
        "mutations": results
    }

    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "docs", "MUTATION_TEST_REPORT.json")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

    print(f"\nSaved machine-readable mutation report to: {report_path}")
    return mutation_score >= 85.0

if __name__ == "__main__":
    success = run_mutation_tests()
    if not success:
        sys.exit(1)
