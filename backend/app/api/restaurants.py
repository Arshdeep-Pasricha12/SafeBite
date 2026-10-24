import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.models import Restaurant, RestaurantImage, User, Inspection, Violation, Complaint, CorrectionRequest
from app.schemas.schemas import (
    RestaurantCreate, RestaurantUpdate, RestaurantOut, 
    RestaurantMatchRequest, RestaurantMatchResponse,
    CorrectionRequestCreate, CorrectionRequestOut, FoodSafetyAssessmentOut
)
from app.api.auth import get_current_user, get_current_owner, get_optional_current_user
from app.core.assessment import FoodSafetyAssessmentEngine

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Helper to map safety rating
def get_safety_rating(score: int) -> str:
    if score >= 90:
        return "Excellent"
    elif score >= 75:
        return "Good"
    elif score >= 60:
        return "Fair"
    else:
        return "Poor"

# Cuisine images for newly created restaurants
CUISINE_IMAGES = {
    "thai": "https://images.unsplash.com/photo-1559311648-d46f4d8593d6?auto=format&fit=crop&w=800&q=80",
    "desserts": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=800&q=80",
    "fast food": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
    "south indian": "https://images.unsplash.com/photo-1668236543090-82eba5ee5976?auto=format&fit=crop&w=800&q=80",
    "continental": "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=80",
    "chinese": "https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&q=80",
    "mexican": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?auto=format&fit=crop&w=800&q=80",
    "vegan": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=800&q=80",
    "lebanese": "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?auto=format&fit=crop&w=800&q=80",
    "north indian": "https://images.unsplash.com/photo-1585938338392-50a59990d4e5?auto=format&fit=crop&w=800&q=80",
    "bbq": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=800&q=80",
    "korean": "https://images.unsplash.com/photo-1530305408560-82d13781b33a?auto=format&fit=crop&w=800&q=80",
    "pizza": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80",
    "burger": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80",
    "street food": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=800&q=80",
    "seafood": "https://images.unsplash.com/photo-1534080564583-6be75777b70a?auto=format&fit=crop&w=800&q=80",
    "japanese": "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=800&q=80",
    "bakery": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=800&q=80",
    "italian": "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?auto=format&fit=crop&w=800&q=80",
    "cafe": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=800&q=80",
    "default": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80"
}

@router.get("", response_model=List[RestaurantOut])
def get_restaurants(
    db: Session = Depends(get_db),
    owned: bool = Query(False, description="Filter by owned restaurants for current logged-in owner"),
    search: Optional[str] = Query(None, description="Search term for name, cuisine, or city"),
    city: Optional[str] = Query(None, description="Filter by city"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine"),
    sort_by: Optional[str] = Query(None, description="Sort option: 'safety_score_desc', 'safety_score_asc', 'name'"),
    current_user: Optional[User] = Depends(get_optional_current_user),
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Restaurant)

    # If owned=True requested, require authentication and restrict to current user's restaurants
    if owned:
        if not current_user or current_user.role not in ["owner", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Must be logged in as an owner/admin to view owned restaurants"
            )
        # Admins see all, Owners see only their owned restaurants
        if current_user.role == "owner":
            query = query.filter(Restaurant.owner_id == current_user.id)
    else:
        # Customers & Guests only see approved restaurants
        query = query.filter(Restaurant.approval_status == "Approved")

    # Apply filters
    if city:
        query = query.filter(Restaurant.city.ilike(f"%{city}%"))
    if cuisine:
        query = query.filter(Restaurant.cuisine.ilike(f"%{cuisine}%"))
    if search:
        query = query.filter(
            Restaurant.name.ilike(f"%{search}%") | 
            Restaurant.cuisine.ilike(f"%{search}%") | 
            Restaurant.city.ilike(f"%{search}%")
        )

    # Apply sorting
    if sort_by == "safety_score_desc":
        query = query.order_by(Restaurant.safety_score.desc())
    elif sort_by == "safety_score_asc":
        query = query.order_by(Restaurant.safety_score.asc())
    elif sort_by == "name":
        query = query.order_by(Restaurant.name.asc())
    else:
        query = query.order_by(Restaurant.id.desc())

    restaurants = query.offset(skip).limit(limit).all()
    return restaurants

def compute_restaurant_assessment(restaurant: Restaurant, db: Session) -> dict:
    """Run explainable risk assessment for a restaurant model."""
    inspections = db.query(Inspection).filter(
        Inspection.restaurant_id == restaurant.id
    ).order_by(Inspection.inspection_date.desc()).all()

    insp_list = []
    for insp in inspections:
        violations = db.query(Violation).filter(Violation.inspection_id == insp.id).all()
        insp_list.append({
            "id": insp.id,
            "inspection_date": insp.inspection_date,
            "inspection_type": insp.inspection_type,
            "total_score": insp.total_score,
            "pass_fail_status": insp.pass_fail_status,
            "risk_level": insp.risk_level,
            "violations": [{
                "severity": v.severity_level,
                "description": v.description,
                "points_deducted": v.points_deducted,
                "repeat_violation": v.repeat_violation
            } for v in violations]
        })

    complaints = db.query(Complaint).filter(Complaint.restaurant_id == restaurant.id).all()
    comp_list = [{
        "status": c.status,
        "complaint_type": c.complaint_type,
        "description": c.description
    } for c in complaints]

    rest_dict = {
        "id": restaurant.id,
        "name": restaurant.name,
        "license_status": restaurant.license_status,
        "previous_violations": restaurant.previous_violations,
        "latest_violation": restaurant.latest_violation,
        "violation_severity": restaurant.violation_severity,
        "is_synthetic": restaurant.is_synthetic,
        "source_name": restaurant.source_name,
        "verification_status": restaurant.verification_status
    }

    return FoodSafetyAssessmentEngine.evaluate(rest_dict, insp_list, comp_list)

def normalize_text(text: str) -> str:
    import re
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    tokens = [w for w in text.split() if w not in {"the", "restaurant", "cafe", "kitchen", "outlet", "express", "bistro", "and", "food"}]
    return " ".join(tokens)

def find_best_restaurant_match(name: str, city: Optional[str], db: Session):
    import difflib
    norm_query = normalize_text(name)
    if not norm_query:
        return None, 0.0

    query = db.query(Restaurant).filter(Restaurant.approval_status == "Approved")
    if city:
        city_filtered = query.filter(Restaurant.city.ilike(f"%{city}%")).all()
        candidates = city_filtered if city_filtered else query.all()
    else:
        candidates = query.all()

    best_match = None
    best_score = 0.0

    for r in candidates:
        norm_r = normalize_text(r.name)
        if norm_query == norm_r:
            return r, 0.98
        if norm_query in norm_r or norm_r in norm_query:
            score = 0.88
            if score > best_score:
                best_score = score
                best_match = r
        ratio = difflib.SequenceMatcher(None, norm_query, norm_r).ratio()
        if ratio > best_score and ratio >= 0.65:
            best_score = ratio
            best_match = r

    return best_match, round(best_score, 2)

@router.get("/match", response_model=RestaurantMatchResponse)
def match_restaurant_get(
    name: str = Query(..., description="Restaurant name to match from food delivery site or companion demo"),
    city: Optional[str] = Query(None, description="Optional city"),
    address: Optional[str] = Query(None, description="Optional address"),
    platform: Optional[str] = Query("generic", description="Calling platform (swiggy, zomato, companion_demo)"),
    db: Session = Depends(get_db)
):
    """
    Match restaurant endpoint for browser extension and companion ordering demo.
    Returns matched restaurant, match confidence, and explainable safety assessment.
    """
    restaurant, confidence = find_best_restaurant_match(name, city, db)
    if not restaurant or confidence < 0.60:
        return RestaurantMatchResponse(
            matched=False,
            match_confidence=confidence,
            restaurant=None,
            assessment=None,
            source_attribution="SafeBite Transparency Engine",
            notice=f"No matching restaurant found in SafeBite registry for '{name}'."
        )

    assessment_data = compute_restaurant_assessment(restaurant, db)
    restaurant_out = RestaurantOut.model_validate(restaurant)
    restaurant_out.assessment = FoodSafetyAssessmentOut(**assessment_data)

    return RestaurantMatchResponse(
        matched=True,
        match_confidence=confidence,
        restaurant=restaurant_out,
        assessment=FoodSafetyAssessmentOut(**assessment_data),
        source_attribution=restaurant.source_name or "SafeBite Transparency Engine",
        notice=assessment_data["provenance_disclaimer"]
    )

@router.post("/match", response_model=RestaurantMatchResponse)
def match_restaurant_post(
    req: RestaurantMatchRequest,
    db: Session = Depends(get_db)
):
    """
    POST variant of match endpoint accepting JSON body.
    """
    return match_restaurant_get(name=req.name, city=req.city, address=req.address, platform=req.platform, db=db)

@router.get("/{id}", response_model=RestaurantOut)
def get_restaurant(id: str, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_optional_current_user)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    # Restrict visibility if restaurant is not approved yet
    if restaurant.approval_status != "Approved":
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )
        if current_user.role == "owner" and restaurant.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access Denied"
            )
        if current_user.role == "customer":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restaurant not found"
            )

    # Attach dynamic explainable assessment
    assessment_data = compute_restaurant_assessment(restaurant, db)
    restaurant_out = RestaurantOut.model_validate(restaurant)
    restaurant_out.assessment = FoodSafetyAssessmentOut(**assessment_data)
    return restaurant_out

@router.post("", response_model=RestaurantOut, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    restaurant_in: RestaurantCreate, 
    db: Session = Depends(get_db),
    current_owner: User = Depends(get_current_owner)
):
    # Check if license number is unique
    existing = db.query(Restaurant).filter(Restaurant.license_number == restaurant_in.license_number).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A restaurant listing with this license number already exists."
        )

    # Generate sequential Rxxxx ID for consistency
    last_restaurant = db.query(Restaurant).order_by(Restaurant.id.desc()).first()
    if last_restaurant and last_restaurant.id.startswith("R"):
        try:
            last_num = int(last_restaurant.id[1:])
            new_num = last_num + 1
            new_id = f"R{new_num:04d}"
        except ValueError:
            new_id = f"R{int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"
    else:
        new_id = "R0101"

    # Default values for safety score for newly created restaurants
    safety_score = 80  # Default score for new listings
    safety_rating = get_safety_rating(safety_score)

    db_restaurant = Restaurant(
        id=new_id,
        name=restaurant_in.name,
        cuisine=restaurant_in.cuisine,
        address=restaurant_in.address,
        city=restaurant_in.city,
        state=restaurant_in.state,
        phone=restaurant_in.phone,
        email=restaurant_in.email,
        description=restaurant_in.description,
        opening_hours=restaurant_in.opening_hours,
        license_number=restaurant_in.license_number,
        license_status=restaurant_in.license_status,
        restaurant_status=restaurant_in.restaurant_status,
        safety_score=safety_score,
        safety_rating=safety_rating,
        approval_status="Pending",  # Requires Admin Approval
        owner_id=current_owner.id
    )
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)

    # Insert images
    if restaurant_in.images:
        for idx, img in enumerate(restaurant_in.images):
            db_image = RestaurantImage(
                restaurant_id=db_restaurant.id,
                image_url=img.image_url,
                is_primary=(idx == 0 or img.is_primary)
            )
            db.add(db_image)
    else:
        # Fallback to cuisine-themed Unsplash images
        primary_url = CUISINE_IMAGES.get(db_restaurant.cuisine.lower(), CUISINE_IMAGES["default"])
        db_image = RestaurantImage(
            restaurant_id=db_restaurant.id,
            image_url=primary_url,
            is_primary=True
        )
        db.add(db_image)

    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

@router.put("/{id}", response_model=RestaurantOut)
def update_restaurant(
    id: str,
    restaurant_in: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    # Validate permission: Owner of this restaurant or Admin
    if current_user.role == "owner" and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this restaurant."
        )
    if current_user.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )

    # Update attributes
    update_data = restaurant_in.model_dump(exclude_unset=True)
    
    # Handle images separately if passed
    images_to_update = update_data.pop("images", None)

    for field, value in update_data.items():
        setattr(restaurant, field, value)

    # Critical fields modification (like license numbers or name changes) resets status to 'Pending'
    if current_user.role == "owner" and ("name" in update_data or "license_number" in update_data):
        restaurant.approval_status = "Pending"

    # Save details
    db.commit()
    db.refresh(restaurant)

    # Update images if provided
    if images_to_update is not None:
        # Remove old images
        db.query(RestaurantImage).filter(RestaurantImage.restaurant_id == restaurant.id).delete()
        for idx, img in enumerate(images_to_update):
            db_image = RestaurantImage(
                restaurant_id=restaurant.id,
                image_url=img["image_url"],
                is_primary=(idx == 0 or img.get("is_primary", False))
            )
            db.add(db_image)
        db.commit()
        db.refresh(restaurant)

    return restaurant

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    # Owner or Admin permission check
    if current_user.role == "owner" and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this restaurant."
        )
    if current_user.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )

    db.delete(restaurant)
    db.commit()
    return None

@router.post("/{id}/correction-request", response_model=CorrectionRequestOut, status_code=status.HTTP_201_CREATED)
def submit_correction_request(
    id: str,
    req_in: CorrectionRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a data correction request or inspection dispute for a restaurant.
    Restricted to restaurant owners or administrators.
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    if current_user.role == "owner" and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit correction requests for your own restaurant."
        )

    new_request = CorrectionRequest(
        restaurant_id=restaurant.id,
        inspection_id=req_in.inspection_id,
        owner_id=current_user.id,
        request_type=req_in.request_type,
        details=req_in.details,
        evidence_url=req_in.evidence_url,
        status="Pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.get("/{id}/correction-requests", response_model=List[CorrectionRequestOut])
def get_restaurant_correction_requests(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get correction requests for a restaurant.
    Accessible by owner of restaurant or administrators.
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )

    if current_user.role == "owner" and restaurant.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access Denied"
        )

    requests = db.query(CorrectionRequest).filter(
        CorrectionRequest.restaurant_id == id
    ).order_by(CorrectionRequest.id.desc()).all()
    return requests

