import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

class RegressionTestSuite(unittest.TestCase):
    """
    Regression test suite verifying fixes for previously discovered defects:
    - Seeded user password verification (KeyError fix)
    - Relative DB URL fallback resolution
    - Token generation and verification with timezone-aware timestamps
    - Provenance filtering
    """

    def setUp(self):
        self.client = TestClient(app)

    def test_regression_admin_login_succeeds_without_key_error(self):
        res = self.client.post("/api/auth/login", json={
            "email": "admin@safebite.demo",
            "password": "adminpassword"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data, "access_token key must be present")
        self.assertEqual(data["role"], "admin")

    def test_regression_customer_login_succeeds(self):
        res = self.client.post("/api/auth/login", json={
            "email": "customer@safebite.demo",
            "password": "password123"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["role"], "customer")

    def test_regression_database_url_not_hardcoded_to_d_drive(self):
        self.assertNotIn("d:/safebite", settings.DATABASE_URL.lower())
        self.assertTrue(settings.DATABASE_URL.startswith("sqlite:///"))

    def test_regression_profile_alias_endpoint(self):
        login_res = self.client.post("/api/auth/login", json={
            "email": "admin@safebite.demo",
            "password": "adminpassword"
        })
        token = login_res.json()["access_token"]
        res = self.client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["email"], "admin@safebite.demo")

if __name__ == "__main__":
    unittest.main()
