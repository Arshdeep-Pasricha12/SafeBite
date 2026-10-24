import unittest
from fastapi.testclient import TestClient
from app.main import app

class RestaurantMatchingAndExtensionTestCase(unittest.TestCase):
    """
    Integration tests for restaurant matching endpoints used by the browser extension and companion ordering demo.
    """

    def setUp(self):
        self.client = TestClient(app)

    def test_exact_name_match_returns_assessment(self):
        res = self.client.get("/api/restaurants/match", params={
            "name": "Haldiram's Sweets & Restaurant",
            "city": "Delhi"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertTrue(data["matched"])
        self.assertGreaterEqual(data["match_confidence"], 0.90)
        self.assertEqual(data["restaurant"]["name"], "Haldiram's Sweets & Restaurant")
        self.assertEqual(data["restaurant"]["safety_score"], 96)
        self.assertGreaterEqual(data["assessment"]["safety_score"], 90)

    def test_fuzzy_name_match(self):
        res = self.client.get("/api/restaurants/match", params={
            "name": "Chipotle Grill",
            "city": "New York"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertTrue(data["matched"])
        self.assertIn("Chipotle", data["restaurant"]["name"])
        self.assertGreaterEqual(data["match_confidence"], 0.70)

    def test_post_variant_match_endpoint(self):
        payload = {
            "name": "Starbucks Coffee",
            "city": "New York",
            "platform": "companion_demo"
        }
        res = self.client.post("/api/restaurants/match", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertTrue(data["matched"])
        self.assertEqual(data["restaurant"]["name"], "Starbucks Coffee")

    def test_unmatched_restaurant_returns_graceful_response(self):
        res = self.client.get("/api/restaurants/match", params={
            "name": "Nonexistent Fake Lunar Cafe 99999",
            "city": "Atlantis"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()

        self.assertFalse(data["matched"])
        self.assertIsNone(data["restaurant"])
        self.assertIn("No matching restaurant found", data["notice"])

if __name__ == "__main__":
    unittest.main()
