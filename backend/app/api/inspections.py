from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.core.database import get_db
from app.models.models import Inspection, Violation, ViolationCode, Inspector, InspectionPhoto
from app.schemas.schemas import UserOut
from app.api.auth import get_current_user

router = APIRouter()

@router.get("/restaurants/{restaurant_id}/inspections")
def get_restaurant_inspections(
    restaurant_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get all inspections for a specific restaurant"""
    
    inspections = db.query(Inspection).filter(
        Inspection.restaurant_id == restaurant_id
    ).order_by(
        Inspection.inspection_date.desc()
    ).offset(skip).limit(limit).all()
    
    if not inspections:
        return []
    
    result = []
    for inspection in inspections:
        # Get violations for this inspection
        violations = db.query(Violation).filter(
            Violation.inspection_id == inspection.id
        ).all()
        
        # Get inspector info
        inspector = db.query(Inspector).filter(
            Inspector.id == inspection.inspector_id
        ).first()
        
        # Get violation details with codes
        violation_details = []
        for violation in violations:
            violation_code = db.query(ViolationCode).filter(
                ViolationCode.id == violation.violation_code_id
            ).first()
            
            violation_details.append({
                "id": violation.id,
                "code": violation_code.code if violation_code else None,
                "category": violation_code.category if violation_code else None,
                "description": violation.description,
                "location": violation.location_in_restaurant,
                "severity": violation.severity_level,
                "points_deducted": violation.points_deducted,
                "corrected_on_site": violation.corrected_on_site,
                "correction_deadline": violation.correction_deadline,
                "repeat_violation": violation.repeat_violation,
                "health_risk_level": violation_code.health_risk_level if violation_code else None
            })
        
        # Get photos
        photos = db.query(InspectionPhoto).filter(
            InspectionPhoto.inspection_id == inspection.id
        ).all()
        
        photo_details = [{
            "id": photo.id,
            "photo_url": photo.photo_url,
            "caption": photo.caption,
            "photo_type": photo.photo_type,
            "taken_by": photo.taken_by
        } for photo in photos]
        
        result.append({
            "id": inspection.id,
            "inspection_date": inspection.inspection_date,
            "inspection_type": inspection.inspection_type,
            "duration_minutes": inspection.inspection_duration_minutes,
            "total_score": inspection.total_score,
            "pass_fail_status": inspection.pass_fail_status,
            "risk_level": inspection.risk_level,
            "permit_action": inspection.permit_action,
            "reinspection_required": inspection.reinspection_required,
            "reinspection_deadline": inspection.reinspection_deadline,
            "inspector_notes": inspection.inspector_notes,
            "corrective_actions_required": inspection.corrective_actions_required,
            "previous_violations_corrected": inspection.previous_violations_corrected,
            "inspector": {
                "id": inspector.id if inspector else None,
                "name": inspector.name if inspector else None,
                "badge_number": inspector.badge_number if inspector else None,
                "certification_level": inspector.certification_level if inspector else None,
                "department": inspector.department if inspector else None
            } if inspector else None,
            "violations": violation_details,
            "photos": photo_details,
            "violation_count": len(violations),
            "critical_violations": len([v for v in violation_details if v["severity"] == "Critical"]),
            "major_violations": len([v for v in violation_details if v["severity"] == "Major"]),
            "minor_violations": len([v for v in violation_details if v["severity"] == "Minor"])
        })
    
    return result

@router.get("/restaurants/{restaurant_id}/inspections/{inspection_id}")
def get_inspection_details(
    restaurant_id: str,
    inspection_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific inspection"""
    
    inspection = db.query(Inspection).filter(
        Inspection.id == inspection_id,
        Inspection.restaurant_id == restaurant_id
    ).first()
    
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    
    # Get all related data (same as above but for single inspection)
    violations = db.query(Violation).filter(
        Violation.inspection_id == inspection.id
    ).all()
    
    inspector = db.query(Inspector).filter(
        Inspector.id == inspection.inspector_id
    ).first()
    
    violation_details = []
    for violation in violations:
        violation_code = db.query(ViolationCode).filter(
            ViolationCode.id == violation.violation_code_id
        ).first()
        
        violation_details.append({
            "id": violation.id,
            "code": violation_code.code if violation_code else None,
            "category": violation_code.category if violation_code else None,
            "description": violation.description,
            "location": violation.location_in_restaurant,
            "severity": violation.severity_level,
            "points_deducted": violation.points_deducted,
            "corrected_on_site": violation.corrected_on_site,
            "correction_deadline": violation.correction_deadline,
            "corrected_date": violation.corrected_date,
            "verified_corrected": violation.verified_corrected,
            "repeat_violation": violation.repeat_violation,
            "management_response": violation.management_response,
            "health_risk_level": violation_code.health_risk_level if violation_code else None,
            "typical_corrective_action": violation_code.typical_corrective_action if violation_code else None
        })
    
    photos = db.query(InspectionPhoto).filter(
        InspectionPhoto.inspection_id == inspection.id
    ).all()
    
    photo_details = [{
        "id": photo.id,
        "photo_url": photo.photo_url,
        "caption": photo.caption,
        "photo_type": photo.photo_type,
        "taken_by": photo.taken_by,
        "created_at": photo.created_at
    } for photo in photos]
    
    return {
        "id": inspection.id,
        "restaurant_id": inspection.restaurant_id,
        "inspection_date": inspection.inspection_date,
        "inspection_type": inspection.inspection_type,
        "duration_minutes": inspection.inspection_duration_minutes,
        "total_score": inspection.total_score,
        "pass_fail_status": inspection.pass_fail_status,
        "risk_level": inspection.risk_level,
        "permit_action": inspection.permit_action,
        "reinspection_required": inspection.reinspection_required,
        "reinspection_deadline": inspection.reinspection_deadline,
        "inspector_notes": inspection.inspector_notes,
        "corrective_actions_required": inspection.corrective_actions_required,
        "previous_violations_corrected": inspection.previous_violations_corrected,
        "created_at": inspection.created_at,
        "inspector": {
            "id": inspector.id,
            "name": inspector.name,
            "badge_number": inspector.badge_number,
            "certification_level": inspector.certification_level,
            "department": inspector.department,
            "contact_email": inspector.contact_email
        } if inspector else None,
        "violations": violation_details,
        "photos": photo_details,
        "summary": {
            "total_violations": len(violations),
            "critical_violations": len([v for v in violation_details if v["severity"] == "Critical"]),
            "major_violations": len([v for v in violation_details if v["severity"] == "Major"]),
            "minor_violations": len([v for v in violation_details if v["severity"] == "Minor"]),
            "total_points_deducted": sum([v["points_deducted"] for v in violation_details]),
            "corrected_on_site": len([v for v in violation_details if v["corrected_on_site"]]),
            "requires_follow_up": len([v for v in violation_details if not v["corrected_on_site"]])
        }
    }

@router.get("/violation-codes")
def get_violation_codes(
    category: Optional[str] = None,
    severity: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all violation codes with optional filtering"""
    
    query = db.query(ViolationCode)
    
    if category:
        query = query.filter(ViolationCode.category == category)
    
    if severity:
        query = query.filter(ViolationCode.severity == severity)
    
    codes = query.all()
    
    return [{
        "id": code.id,
        "code": code.code,
        "category": code.category,
        "description": code.description,
        "severity": code.severity,
        "points_deducted": code.points_deducted,
        "health_risk_level": code.health_risk_level,
        "typical_corrective_action": code.typical_corrective_action
    } for code in codes]

@router.get("/inspectors")
def get_inspectors(
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    """Get list of inspectors (Admin only)"""
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    query = db.query(Inspector)
    
    if active_only:
        query = query.filter(Inspector.active == True)
    
    inspectors = query.all()
    
    return [{
        "id": inspector.id,
        "name": inspector.name,
        "badge_number": inspector.badge_number,
        "certification_level": inspector.certification_level,
        "department": inspector.department,
        "contact_email": inspector.contact_email,
        "active": inspector.active,
        "created_at": inspector.created_at
    } for inspector in inspectors]