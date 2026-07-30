from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.models import Restaurant, User
from app.schemas.schemas import RestaurantOut, UserOut
from app.api.auth import get_current_admin

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
