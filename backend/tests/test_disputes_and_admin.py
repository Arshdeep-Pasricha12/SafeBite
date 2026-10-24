import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal
from app.models.models import CorrectionRequest, User, Restaurant

class DisputesAndAdminTestCase(unittest.TestCase):
    """
    Integration tests for owner dispute/correction workflows and administrator review.
    """

    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()

        # Login admin
        admin_login = self.client.post("/api/auth/login", json={
            "email": "admin@safebite.demo",
            "password": "adminpassword"
        })
        self.admin_token = admin_login.json()["access_token"]

        # Register & login test owner
        owner_data = {
            "email": "test_dispute_owner@safebite.demo",
            "password": "ownerpassword123",
            "full_name": "Dispute Test Owner",
            "role": "owner"
        }
        self.client.post("/api/auth/register", json=owner_data)
        owner_login = self.client.post("/api/auth/login", json={
            "email": "test_dispute_owner@safebite.demo",
            "password": "ownerpassword123"
        })
        self.owner_token = owner_login.json()["access_token"]

        # Create a test restaurant owned by this owner
        rest_payload = {
            "name": "Dispute Test Kitchen",
            "cuisine": "North Indian",
            "address": "42 Test Lane",
            "city": "Delhi",
            "state": "Delhi",
            "phone": "011-99887766",
            "email": "test_dispute_owner@safebite.demo",
            "license_number": "FSSAI_DISP_991823",
            "license_status": "Active",
            "restaurant_status": "Open",
            "images": []
        }
        create_res = self.client.post(
            "/api/restaurants", 
            json=rest_payload, 
            headers={"Authorization": f"Bearer {self.owner_token}"}
        )
        self.restaurant_id = create_res.json()["id"]

    def tearDown(self):
        # Cleanup
        self.db.query(CorrectionRequest).filter(CorrectionRequest.restaurant_id == self.restaurant_id).delete()
        self.db.query(Restaurant).filter(Restaurant.id == self.restaurant_id).delete()
        self.db.query(User).filter(User.email == "test_dispute_owner@safebite.demo").delete()
        self.db.commit()
        self.db.close()

    def test_owner_submits_correction_request_and_admin_reviews(self):
        # 1. Owner submits correction request
        req_payload = {
            "restaurant_id": self.restaurant_id,
            "request_type": "Data Correction",
            "details": "Opening hours updated to 8:00 AM - 11:30 PM after kitchen expansion.",
            "evidence_url": "https://safebite.demo/evidence/hours.pdf"
        }
        res = self.client.post(
            f"/api/restaurants/{self.restaurant_id}/correction-request",
            json=req_payload,
            headers={"Authorization": f"Bearer {self.owner_token}"}
        )
        self.assertEqual(res.status_code, 201)
        correction_id = res.json()["id"]
        self.assertEqual(res.json()["status"], "Pending")

        # 2. Owner retrieves their correction requests
        res = self.client.get(
            f"/api/restaurants/{self.restaurant_id}/correction-requests",
            headers={"Authorization": f"Bearer {self.owner_token}"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json()), 1)

        # 3. Admin lists pending correction requests
        res = self.client.get(
            "/api/admin/correction-requests",
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res.status_code, 200)
        request_ids = [r["id"] for r in res.json()]
        self.assertIn(correction_id, request_ids)

        # 4. Admin reviews and approves correction request
        review_payload = {
            "status": "Approved",
            "admin_notes": "Verified new operating license schedule. Approved."
        }
        res = self.client.put(
            f"/api/admin/correction-requests/{correction_id}/review",
            json=review_payload,
            headers={"Authorization": f"Bearer {self.admin_token}"}
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "Approved")
        self.assertIsNotNone(res.json()["reviewed_at"])

if __name__ == "__main__":
    unittest.main()
