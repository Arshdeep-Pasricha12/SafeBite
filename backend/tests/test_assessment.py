import unittest
import datetime
from app.core.assessment import FoodSafetyAssessmentEngine

class FoodSafetyAssessmentEngineTestCase(unittest.TestCase):
    """
    Unit test suite for the explainable, deterministic food-safety risk engine.
    """

    def test_clean_inspection_evaluates_to_excellent(self):
        restaurant = {
            "name": "Clean Test Cafe",
            "license_status": "Active",
            "is_synthetic": False,
            "source_name": "NYC Health DOHMH OpenData"
        }
        inspections = [{
            "inspection_date": datetime.date.today(),
            "violations": []
        }]
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, inspections, [])

        self.assertEqual(result["safety_score"], 100)
        self.assertEqual(result["safety_rating"], "Excellent")
        self.assertIn("Pass", result["grade_label"])
        self.assertEqual(result["risk_level"], "Low")
        self.assertEqual(result["critical_violations_count"], 0)
        self.assertTrue(any("Zero critical food safety violations" in f for f in result["positive_factors"]))
        self.assertIn("OFFICIAL DATA", result["provenance_disclaimer"])

    def test_critical_violation_deduction(self):
        restaurant = {
            "name": "Violating Kitchen",
            "license_status": "Active",
            "is_synthetic": True
        }
        inspections = [{
            "inspection_date": datetime.date.today(),
            "violations": [{
                "severity": "Critical",
                "description": "Improper holding temperature for raw poultry",
                "repeat_violation": False
            }]
        }]
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, inspections, [])

        self.assertEqual(result["safety_score"], 82)
        self.assertEqual(result["critical_violations_count"], 1)
        self.assertIn("Critical Violation", result["risk_factors"][0])

    def test_repeat_violation_applies_escalating_multiplier(self):
        restaurant = {
            "name": "Repeat Offender Grill",
            "license_status": "Active",
            "is_synthetic": True
        }
        inspections = [{
            "inspection_date": datetime.date.today(),
            "violations": [{
                "severity": "Critical",
                "description": "Active vermin infestation",
                "repeat_violation": True
            }]
        }]
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, inspections, [])

        self.assertEqual(result["safety_score"], 73)
        self.assertEqual(result["repeat_violations_count"], 1)
        self.assertIn("REPEAT OFFENSE", result["risk_factors"][0])

    def test_stale_inspection_triggers_penalty_and_warning(self):
        restaurant = {
            "name": "Stale Record Diner",
            "license_status": "Active",
            "is_synthetic": False
        }
        stale_date = datetime.date.today() - datetime.timedelta(days=420)
        inspections = [{
            "inspection_date": stale_date,
            "violations": []
        }]
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, inspections, [])

        self.assertEqual(result["data_freshness_status"], "Stale")
        self.assertIn("Stale Data", result["grade_label"])
        self.assertTrue(any("Inspection is 420 days old" in factor for factor in result["risk_factors"]))

    def test_expired_inspection_penalizes_score(self):
        restaurant = {
            "name": "Expired Record Bistro",
            "license_status": "Active",
            "is_synthetic": False
        }
        expired_date = datetime.date.today() - datetime.timedelta(days=800)
        inspections = [{
            "inspection_date": expired_date,
            "violations": []
        }]
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, inspections, [])

        self.assertEqual(result["data_freshness_status"], "Expired")
        self.assertTrue(result["confidence_score"] <= 0.40)

    def test_uninspected_restaurant_fallback(self):
        restaurant = {
            "name": "Newly Opened Eatery",
            "license_status": "Active",
            "is_synthetic": True
        }
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, [], [])

        self.assertEqual(result["data_freshness_status"], "Uninspected")
        self.assertEqual(result["grade_label"], "Uninspected / Pending")
        self.assertIn("pending", result["consumer_advice"].lower())

    def test_suspended_license_overrides_to_high_risk_alert(self):
        restaurant = {
            "name": "Suspended Outlet",
            "license_status": "Suspended",
            "is_synthetic": True
        }
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, [], [])

        self.assertLessEqual(result["safety_score"], 35)
        self.assertEqual(result["safety_rating"], "Poor")
        self.assertEqual(result["grade_label"], "High Risk / Alert")
        self.assertEqual(result["risk_level"], "Critical")
        self.assertIn("DO NOT ORDER", result["consumer_advice"])

    def test_verified_complaint_deduction(self):
        restaurant = {
            "name": "Complained Cafe",
            "license_status": "Active",
            "is_synthetic": True
        }
        inspections = [{
            "inspection_date": datetime.date.today(),
            "violations": []
        }]
        complaints = [
            {"status": "Verified", "description": "Foreign object found in meal"}
        ]
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, inspections, complaints)

        self.assertEqual(result["safety_score"], 94)  # 100 - 6 = 94
        self.assertEqual(result["active_complaints_count"], 1)

    def test_synthetic_provenance_disclaimer(self):
        restaurant = {
            "name": "Demo Benchmark Restaurant",
            "is_synthetic": True,
            "verification_status": "Synthetic Demonstration",
            "source_name": "SafeBite Benchmark"
        }
        result = FoodSafetyAssessmentEngine.evaluate(restaurant, [], [])

        self.assertIn("DEMONSTRATION RECORD", result["provenance_disclaimer"])
        self.assertIn("simulated benchmark data", result["provenance_disclaimer"])

if __name__ == "__main__":
    unittest.main()
