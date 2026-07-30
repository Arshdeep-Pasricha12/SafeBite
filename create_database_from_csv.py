#!/usr/bin/env python3
"""
SafeBite Centralized Database Creator
Creates ONE database from CSV files in /data directory
This is the SINGLE SOURCE OF TRUTH for the database
"""

import sys
import os
import pandas as pd
from datetime import datetime, date

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.core.database import SessionLocal, engine, Base
from app.models.models import (
    User, Restaurant, RestaurantImage, Inspector, Inspection, 
    ViolationCode, Violation, InspectionPhoto, Complaint
)
from app.core.security import get_password_hash

def create_centralized_database():
    """
    Create the SafeBite database from CSV files
    This is the SINGLE database creation script
    """
    
    print("🏗️  Creating SafeBite database from CSV files...")
    print("📁 Source: d:/safebite/data/*.csv")
    print("🎯 Target: d:/safebite/database/safebite.db (SINGLE DATABASE)")
    
    # Create all tables (drop existing first)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 1. Load Users
        print("\n👥 Loading users...")
        users_df = pd.read_csv('data/users.csv')
        for _, row in users_df.iterrows():
            user = User(
                email=row['Email'],
                password_hash=row['PasswordHash'],
                full_name=row['FullName'],
                role=row['Role']
            )
            db.add(user)
        
        db.commit()
        print(f"✅ Created {len(users_df)} users")
        
        # 2. Load Violation Codes
        print("\n📋 Loading violation codes...")
        codes_df = pd.read_csv('data/violation_codes.csv')
        violation_codes = {}
        for _, row in codes_df.iterrows():
            code = ViolationCode(
                code=row['Code'],
                category=row['Category'],
                description=row['Description'],
                severity=row['Severity'],
                points_deducted=row['PointsDeducted'],
                health_risk_level=row['HealthRiskLevel'],
                typical_corrective_action=row['TypicalCorrectiveAction']
            )
            db.add(code)
            violation_codes[row['Code']] = code
        
        db.commit()
        print(f"✅ Created {len(codes_df)} violation codes")
        
        # 3. Load Inspectors
        print("\n👨‍💼 Loading inspectors...")
        inspectors_df = pd.read_csv('data/inspectors.csv')
        inspectors = {}
        for _, row in inspectors_df.iterrows():
            inspector = Inspector(
                name=row['Name'],
                badge_number=row['BadgeNumber'],
                certification_level=row['CertificationLevel'],
                department=row['Department'],
                contact_email=row['ContactEmail'],
                active=row['Active']
            )
            db.add(inspector)
            inspectors[row['InspectorID']] = inspector
        
        db.commit()
        print(f"✅ Created {len(inspectors_df)} inspectors")
        
        # 4. Load Restaurants
        print("\n🏪 Loading restaurants...")
        restaurants_df = pd.read_csv('data/restaurants.csv')
        restaurants = {}
        for _, row in restaurants_df.iterrows():
            # Find owner
            owner = db.query(User).filter(User.email == row['Email']).first()
            
            restaurant = Restaurant(
                id=row['RestaurantID'],
                name=row['RestaurantName'],
                cuisine=row['Cuisine'],
                address=row['Address'],
                city=row['City'],
                state=row['State'],
                phone=row['Phone'],
                email=row['Email'],
                description=f"Welcome to {row['RestaurantName']}! We serve authentic {row['Cuisine']} cuisine.",
                opening_hours="09:00 AM - 10:00 PM",
                license_number=row['LicenseNumber'],
                license_status=row['LicenseStatus'],
                restaurant_status=row['RestaurantStatus'],
                safety_score=row['SafetyScore'],
                safety_rating=row['SafetyRating'],
                approval_status="Approved",
                owner_id=owner.id if owner else None
            )
            db.add(restaurant)
            restaurants[row['RestaurantID']] = restaurant
            
            # Add restaurant image
            img = RestaurantImage(
                restaurant_id=restaurant.id,
                image_url="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
                is_primary=True
            )
            db.add(img)
        
        db.commit()
        print(f"✅ Created {len(restaurants_df)} restaurants")
        
        # 5. Load Inspections
        print("\n🔍 Loading inspections...")
        inspections_df = pd.read_csv('data/inspections.csv')
        inspections = {}
        for _, row in inspections_df.iterrows():
            restaurant = restaurants[row['RestaurantID']]
            inspector = inspectors[row['InspectorID']]
            
            inspection = Inspection(
                restaurant_id=row['RestaurantID'],
                inspector_id=inspector.id,
                inspection_date=pd.to_datetime(row['InspectionDate']).date(),
                inspection_type=row['InspectionType'],
                inspection_duration_minutes=row['DurationMinutes'],
                total_score=row['TotalScore'],
                pass_fail_status=row['PassFailStatus'],
                risk_level=row['RiskLevel'],
                inspector_notes=row['InspectorNotes'],
                reinspection_required=False,
                previous_violations_corrected=True
            )
            db.add(inspection)
            inspections[row['InspectionID']] = inspection
        
        db.commit()
        print(f"✅ Created {len(inspections_df)} inspections")
        
        # 6. Load Violations
        print("\n⚠️  Loading violations...")
        violations_df = pd.read_csv('data/violations.csv')
        for _, row in violations_df.iterrows():
            if pd.isna(row['ViolationCode']) or row['ViolationCode'] == 'None':
                continue
                
            inspection = inspections[row['InspectionID']]
            violation_code = violation_codes.get(row['ViolationCode'])
            
            if not violation_code:
                continue
            
            violation = Violation(
                inspection_id=inspection.id,
                violation_code_id=violation_code.id,
                description=row['Description'],
                location_in_restaurant=row['Location'],
                severity_level=row['Severity'],
                points_deducted=row['PointsDeducted'],
                corrected_on_site=row['CorrectedOnSite'],
                repeat_violation=False
            )
            db.add(violation)
        
        db.commit()
        violations_count = len(violations_df) - violations_df['ViolationCode'].isna().sum()
        print(f"✅ Created {violations_count} violations")
        
        print(f"\n🎉 Database created successfully!")
        print(f"📊 Summary:")
        print(f"   - Users: {len(users_df)}")
        print(f"   - Restaurants: {len(restaurants_df)}")
        print(f"   - Inspectors: {len(inspectors_df)}")
        print(f"   - Inspections: {len(inspections_df)}")
        print(f"   - Violations: {violations_count}")
        print(f"   - Violation Codes: {len(codes_df)}")
        print(f"\n💾 Database location: d:/safebite/database/safebite.db")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_centralized_database()