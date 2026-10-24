from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Restaurant, User, CorrectionRequest
from app.schemas.schemas import RestaurantOut, UserOut, CorrectionRequestOut, CorrectionRequestReview
from app.api.auth import get_current_admin
import datetime

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/pending-restaurants", response_model=List[RestaurantOut])
def get_pending_restaurants(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Get all restaurants with 'Pending' approval status.
    Only accessible by administrators.
    """
    pending = db.query(Restaurant).filter(Restaurant.approval_status == "Pending").all()
    return pending

@router.put("/restaurants/{id}/approve", response_model=RestaurantOut)
def approve_restaurant(
    id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Approve a restaurant listing, making it visible to customers.
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    restaurant.approval_status = "Approved"
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.put("/restaurants/{id}/reject", response_model=RestaurantOut)
def reject_restaurant(
    id: str,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Reject a restaurant listing. It will remain hidden from customers.
    """
    restaurant = db.query(Restaurant).filter(Restaurant.id == id).first()
    if not restaurant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurant not found"
        )
    
    restaurant.approval_status = "Rejected"
    db.commit()
    db.refresh(restaurant)
    return restaurant

@router.get("/users", response_model=List[UserOut])
def get_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Get a list of all registered users.
    Only accessible by administrators.
    """
    users = db.query(User).order_by(User.id.desc()).all()
    return users

@router.get("/correction-requests", response_model=List[CorrectionRequestOut])
def get_admin_correction_requests(
    status_filter: str = "Pending",
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Get all correction requests submitted by restaurant owners.
    """
    query = db.query(CorrectionRequest)
    if status_filter != "all":
        query = query.filter(CorrectionRequest.status == status_filter)
    return query.order_by(CorrectionRequest.id.desc()).all()

@router.put("/correction-requests/{id}/review", response_model=CorrectionRequestOut)
def review_correction_request(
    id: int,
    review_in: CorrectionRequestReview,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """
    Review (approve or reject) a correction request.
    """
    req = db.query(CorrectionRequest).filter(CorrectionRequest.id == id).first()
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Correction request not found"
        )

    req.status = review_in.status
    req.admin_notes = review_in.admin_notes
    req.reviewed_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(req)
    return req

