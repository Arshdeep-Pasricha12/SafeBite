import os
import sys
import json
import argparse
import datetime
from sqlalchemy.orm import Session

# Add app to path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.core.database import SessionLocal, engine, Base
from app.models.models import (
    Restaurant, RestaurantImage, Inspector, Inspection, 
    Violation, ViolationCode, User
)

def run_ingestion(file_path: str, source_override: str = None, dry_run: bool = False, limit: int = None):
    """
    Ingest verified food safety inspection records into SafeBite.
    Validates, deduplicates, and preserves provenance.
    """
    print("=" * 60)
    print("SafeBite Inspection Data Ingestion Pipeline")
    print(f"Data file: {file_path}")
    print(f"Dry Run:   {dry_run}")
    print("=" * 60)

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            records = json.load(f)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON format: {e}")
            return False

    if not isinstance(records, list):
        print("ERROR: Root JSON element must be a list of restaurant records.")
        return False

    if limit and limit > 0:
        records = records[:limit]

    db: Session = SessionLocal()

    stats = {
        "total_parsed": len(records),
        "restaurants_created": 0,
        "restaurants_updated": 0,
        "inspections_created": 0,
        "violations_created": 0,
        "skipped": 0,
        "errors": 0
    }

    # Ensure admin / system user exists for owner assignment
    system_admin = db.query(User).filter(User.role == "admin").first()
    owner_id = system_admin.id if system_admin else 1

    try:
        for idx, item in enumerate(records, start=1):
            name = item.get("name", "").strip()
            license_no = item.get("license_number", "").strip()
            rest_id = item.get("id") or f"R_VER_{idx:03d}"

            if not name or not license_no:
                print(f"[Record {idx}] SKIPPED: Missing required name or license_number.")
                stats["skipped"] += 1
                continue

            source_name = source_override or item.get("source_name") or "Verified Official Dataset"
            source_url = item.get("source_url") or "https://safebite.demo/sources/verified"
            source_record_id = item.get("source_record_id") or license_no
            verification_status = item.get("verification_status") or "Verified Official"
            is_synthetic = bool(item.get("is_synthetic", False))
            confidence_score = float(item.get("confidence_score", 0.95))
            data_freshness_status = item.get("data_freshness_status", "Current")

            last_insp_date = None
            if item.get("last_inspection_date"):
                try:
                    last_insp_date = datetime.date.fromisoformat(item["last_inspection_date"])
                except Exception:
                    pass

            # Check if restaurant with this ID or license exists
            existing = db.query(Restaurant).filter(
                (Restaurant.id == rest_id) | (Restaurant.license_number == license_no)
            ).first()

            if existing:
                action = "UPDATE"
                target_restaurant = existing
                stats["restaurants_updated"] += 1
            else:
                action = "CREATE"
                target_restaurant = Restaurant(id=rest_id, owner_id=owner_id)
                stats["restaurants_created"] += 1

            # Populate fields
            target_restaurant.name = name
            target_restaurant.cuisine = item.get("cuisine", "Multi-Cuisine")
            target_restaurant.address = item.get("address", "Official Address On File")
            target_restaurant.city = item.get("city", "Delhi")
            target_restaurant.state = item.get("state", "Delhi")
            target_restaurant.phone = item.get("phone", "+91-00-00000000")
            target_restaurant.email = item.get("email", f"info@{license_no.lower()}.safebite.demo")
            target_restaurant.description = item.get("description", "")
            target_restaurant.opening_hours = item.get("opening_hours", "09:00 AM - 10:00 PM")
            target_restaurant.license_number = license_no
            target_restaurant.license_status = item.get("license_status", "Active")
            target_restaurant.restaurant_status = item.get("restaurant_status", "Open")
            target_restaurant.safety_score = int(item.get("safety_score", 90))
            target_restaurant.safety_rating = item.get("safety_rating", "Excellent")
            target_restaurant.last_inspection_date = last_insp_date
            target_restaurant.inspection_result = item.get("inspection_result", "Passed")
            target_restaurant.inspection_score = item.get("inspection_score", target_restaurant.safety_score)
            target_restaurant.previous_violations = int(item.get("previous_violations", 0))
            target_restaurant.latest_violation = item.get("latest_violation")
            target_restaurant.violation_severity = item.get("violation_severity")
            target_restaurant.complaint_count = int(item.get("complaint_count", 0))
            target_restaurant.approval_status = "Approved"

            # Provenance fields
            target_restaurant.source_name = source_name
            target_restaurant.source_url = source_url
            target_restaurant.source_record_id = source_record_id
            target_restaurant.last_synced_at = datetime.datetime.now(datetime.timezone.utc)
            target_restaurant.verification_status = verification_status
            target_restaurant.confidence_score = confidence_score
            target_restaurant.is_synthetic = is_synthetic
            target_restaurant.data_freshness_status = data_freshness_status

            print(f"[{action}] {target_restaurant.id}: {name} ({verification_status}, Source: {source_name})")

            if not dry_run:
                if action == "CREATE":
                    db.add(target_restaurant)
                db.flush()

                # Add images
                images = item.get("images", [])
                if images:
                    # Remove existing images if updating
                    db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == target_restaurant.id).delete()
                    for img_idx, img_url in enumerate(images):
                        db.add(RestaurantImage(
                            restaurant_id=target_restaurant.id,
                            image_url=img_url,
                            is_primary=(img_idx == 0)
                        ))

                # Process inspections
                for insp_item in item.get("inspections", []):
                    # Inspector handling
                    insp_badge = insp_item.get("inspector_badge", "INS-OFF-001")
                    inspector = db.query(Inspector).filter(Inspector.badge_number == insp_badge).first()
                    if not inspector:
                        inspector = Inspector(
                            name=insp_item.get("inspector_name", "Official Inspector"),
                            badge_number=insp_badge,
                            certification_level="Lead",
                            department=insp_item.get("inspector_department", "Public Health Department"),
                            active=True
                        )
                        db.add(inspector)
                        db.flush()

                    insp_date_val = datetime.date.today()
                    if insp_item.get("inspection_date"):
                        try:
                            insp_date_val = datetime.date.fromisoformat(insp_item["inspection_date"])
                        except Exception:
                            pass

                    # Create Inspection
                    inspection_rec = Inspection(
                        restaurant_id=target_restaurant.id,
                        inspector_id=inspector.id,
                        inspection_date=insp_date_val,
                        inspection_type=insp_item.get("inspection_type", "Routine"),
                        inspection_duration_minutes=insp_item.get("duration_minutes", 90),
                        total_score=int(insp_item.get("total_score", 90)),
                        pass_fail_status=insp_item.get("pass_fail_status", "Passed"),
                        risk_level=insp_item.get("risk_level", "Low"),
                        inspector_notes=insp_item.get("inspector_notes"),
                        source_name=source_name,
                        source_record_id=source_record_id,
                        verification_status=verification_status,
                        is_synthetic=is_synthetic
                    )
                    db.add(inspection_rec)
                    db.flush()
                    stats["inspections_created"] += 1

                    # Violations
                    for v_item in insp_item.get("violations", []):
                        v_code_str = v_item.get("code", "2-102.11")
                        v_code = db.query(ViolationCode).filter(ViolationCode.code == v_code_str).first()
                        if not v_code:
                            v_code = ViolationCode(
                                code=v_code_str,
                                category=v_item.get("category", "General Sanitation"),
                                description=v_item.get("description", "Sanitation requirement"),
                                severity=v_item.get("severity", "Minor"),
                                points_deducted=v_item.get("points_deducted", 2),
                                health_risk_level="Low"
                            )
                            db.add(v_code)
                            db.flush()

                        violation_rec = Violation(
                            inspection_id=inspection_rec.id,
                            violation_code_id=v_code.id,
                            description=v_item.get("description", ""),
                            severity_level=v_item.get("severity", "Minor"),
                            points_deducted=v_item.get("points_deducted", 2),
                            corrected_on_site=bool(v_item.get("corrected_on_site", True)),
                            repeat_violation=bool(v_item.get("repeat_violation", False))
                        )
                        db.add(violation_rec)
                        stats["violations_created"] += 1

        if not dry_run:
            db.commit()
            print("\nSuccessfully committed changes to database.")
        else:
            db.rollback()
            print("\nDry-run complete. No changes written to database.")

    except Exception as e:
        db.rollback()
        print(f"\nERROR during ingestion: {e}")
        stats["errors"] += 1
        return False
    finally:
        db.close()

    print("\n" + "=" * 40)
    print("Ingestion Summary Statistics:")
    print(f"  Total records parsed:       {stats['total_parsed']}")
    print(f"  Restaurants created:        {stats['restaurants_created']}")
    print(f"  Restaurants updated:        {stats['restaurants_updated']}")
    print(f"  Inspections created:        {stats['inspections_created']}")
    print(f"  Violations created:         {stats['violations_created']}")
    print(f"  Records skipped:            {stats['skipped']}")
    print(f"  Errors encountered:         {stats['errors']}")
    print("=" * 40)
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SafeBite Traceable Inspection Data Ingestion")
    parser.add_argument("--file", default=os.path.join(os.path.dirname(__file__), "data", "verified_inspection_records.json"),
                        help="Path to JSON file with inspection records")
    parser.add_argument("--source", default=None, help="Override source_name provenance tag")
    parser.add_argument("--dry-run", action="store_true", help="Perform validation and dry run without writing to DB")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of records to ingest")

    args = parser.parse_args()
    success = run_ingestion(args.file, args.source, args.dry_run, args.limit)
    if not success:
        sys.exit(1)
