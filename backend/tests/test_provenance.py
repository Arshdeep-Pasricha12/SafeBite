import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.models import Restaurant

class DataProvenanceTestCase(unittest.TestCase):
    """
    Unit and integration tests verifying provenance fields, synthetic flags, and data states.
    """

    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def test_verified_official_records_exist_and_are_marked_non_synthetic(self):
        verified_restaurants = self.db.query(Restaurant).filter(Restaurant.is_synthetic == False).all()
        self.assertGreater(len(verified_restaurants), 0, "Should have at least 1 verified official restaurant")

        for r in verified_restaurants:
            self.assertFalse(r.is_synthetic, f"Restaurant {r.id} must have is_synthetic=False")
            self.assertEqual(r.verification_status, "Verified Official")
            self.assertIsNotNone(r.source_name)
            self.assertIsNotNone(r.source_url)
            self.assertGreaterEqual(r.confidence_score, 0.90)

    def test_synthetic_records_are_explicitly_tagged(self):
        synthetic_sample = self.db.query(Restaurant).filter(Restaurant.is_synthetic == True).limit(5).all()
        self.assertGreater(len(synthetic_sample), 0, "Synthetic benchmark sample must exist")

        for r in synthetic_sample:
            self.assertTrue(r.is_synthetic)
            self.assertEqual(r.verification_status, "Synthetic Demonstration")
            self.assertIn("Synthetic Benchmark", r.source_name)

    def test_restaurant_api_returns_provenance_metadata(self):
        res = self.client.get("/api/restaurants/R_OFF_001")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertFalse(data["is_synthetic"])
        self.assertEqual(data["verification_status"], "Verified Official")
        self.assertIn("FSSAI", data["source_name"])
        self.assertIn("fssai.gov.in", data["source_url"])
        self.assertIn("assessment", data)
        self.assertIn("OFFICIAL DATA", data["assessment"]["provenance_disclaimer"])

if __name__ == "__main__":
    unittest.main()
