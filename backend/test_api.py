import os
import sys
import unittest
from fastapi.testclient import TestClient

# Add app folder to system path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.main import app
from app.core.database import SessionLocal
from app.models.models import User, Restaurant, RestaurantImage

class SafeBiteAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = SessionLocal()
        
        # Clean test data if left over
        test_restaurant = self.db.query(Restaurant).filter(Restaurant.license_number == "FSSAI_TEST_123456").first()
        if test_restaurant:
            self.db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == test_restaurant.id).delete(synchronize_session=False)
            self.db.query(Restaurant).filter(Restaurant.id == test_restaurant.id).delete(synchronize_session=False)
        self.db.query(User).filter(User.email.like("test_%@safebite.demo")).delete(synchronize_session=False)
        self.db.commit()

    def tearDown(self):
        # Cleanup test entries
        test_restaurant = self.db.query(Restaurant).filter(Restaurant.license_number == "FSSAI_TEST_123456").first()
        if test_restaurant:
            self.db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == test_restaurant.id).delete(synchronize_session=False)
            self.db.query(Restaurant).filter(Restaurant.id == test_restaurant.id).delete(synchronize_session=False)
        self.db.query(User).filter(User.email.like("test_%@safebite.demo")).delete(synchronize_session=False)
        self.db.commit()
        self.db.close()

    def test_auth_workflow(self):
        # 1. Register Customer
        customer_payload = {
            "email": "test_cust@safebite.demo",
            "password": "custpassword123",
            "full_name": "Test Customer User",
            "role": "customer"
        }
        res = self.client.post("/api/auth/register", json=customer_payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.json()["email"], "test_cust@safebite.demo")
        self.assertEqual(res.json()["role"], "customer")

        # 2. Login Customer
        login_payload = {
            "email": "test_cust@safebite.demo",
            "password": "custpassword123"
        }
        res = self.client.post("/api/auth/login", json=login_payload)
        self.assertEqual(res.status_code, 200)
        token_data = res.json()
        self.assertIn("access_token", token_data)
        self.assertEqual(token_data["role"], "customer")
        token = token_data["access_token"]

        # 3. Retrieve Profile
        res = self.client.get("/api/users/profile", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["email"], "test_cust@safebite.demo")

        # 4. Retrieve Profile via direct /api/profile alias
        res = self.client.get("/api/profile", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["email"], "test_cust@safebite.demo")

    def test_restaurant_approval_and_discovery_workflow(self):
        # Setup users
        # Register Owner
        owner_payload = {
            "email": "test_owner@safebite.demo",
            "password": "ownerpassword123",
            "full_name": "Test Owner User",
            "role": "owner"
        }
        res = self.client.post("/api/auth/register", json=owner_payload)
        self.assertEqual(res.status_code, 201)
        
        # Login Owner
        res = self.client.post("/api/auth/login", json={"email": "test_owner@safebite.demo", "password": "ownerpassword123"})
        owner_token = res.json()["access_token"]

        # Login Admin (Using seeded admin)
        res = self.client.post("/api/auth/login", json={"email": "admin@safebite.demo", "password": "adminpassword"})
        admin_token = res.json()["access_token"]

        # Login Customer (Using seeded customer)
        res = self.client.post("/api/auth/login", json={"email": "customer@safebite.demo", "password": "password123"})
        customer_token = res.json()["access_token"]

        # 1. Owner Creates Restaurant
        restaurant_payload = {
            "name": "Test Delhi Heights",
            "cuisine": "North Indian",
            "address": "Connaught Place, Central Delhi",
            "city": "Delhi",
            "state": "Delhi",
            "phone": "011-9876543",
            "email": "test_owner@safebite.demo",
            "description": "Premium dining experience",
            "opening_hours": "11:00 AM - 11:00 PM",
            "license_number": "FSSAI_TEST_123456",
            "license_status": "Active",
            "restaurant_status": "Open",
            "images": []
        }
        res = self.client.post("/api/restaurants", json=restaurant_payload, headers={"Authorization": f"Bearer {owner_token}"})
        self.assertEqual(res.status_code, 201)
        created_rest = res.json()
        self.assertEqual(created_rest["name"], "Test Delhi Heights")
        self.assertEqual(created_rest["approval_status"], "Pending") # New listings must be pending
        rest_id = created_rest["id"]

        # 2. Customer searches restaurants -> Pending restaurant should NOT be visible
        res = self.client.get("/api/restaurants?search=Test Delhi Heights")
        self.assertEqual(res.status_code, 200)
        results = res.json()
        self.assertTrue(all(r["id"] != rest_id for r in results))

        # 3. Customer tries to view restaurant detail directly -> Should get 404/403
        res = self.client.get(f"/api/restaurants/{rest_id}")
        self.assertEqual(res.status_code, 404)

        # 4. Admin views pending requests -> Delhi Heights should be in queue
        res = self.client.get("/api/admin/pending-restaurants", headers={"Authorization": f"Bearer {admin_token}"})
        self.assertEqual(res.status_code, 200)
        pending_list = res.json()
        self.assertTrue(any(r["id"] == rest_id for r in pending_list))

        # 5. Admin Approves Restaurant
        res = self.client.put(f"/api/admin/restaurants/{rest_id}/approve", headers={"Authorization": f"Bearer {admin_token}"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["approval_status"], "Approved")

        # 6. Customer searches restaurants -> Delhi Heights should now be visible!
        res = self.client.get("/api/restaurants?search=Test Delhi Heights")
        self.assertEqual(res.status_code, 200)
        results = res.json()
        self.assertTrue(any(r["id"] == rest_id for r in results))

        # 7. Customer views details -> Should work now
        res = self.client.get(f"/api/restaurants/{rest_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["name"], "Test Delhi Heights")
        self.assertEqual(res.json()["safety_rating"], "Good") # 80 score maps to Good

if __name__ == "__main__":
    unittest.main()
