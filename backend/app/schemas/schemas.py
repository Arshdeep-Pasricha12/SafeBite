import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    email: str
    full_name: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: str = Field(..., description="Role must be 'customer', 'owner', or 'admin'")

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# --- Restaurant Image Schemas ---
class RestaurantImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class RestaurantImageCreate(RestaurantImageBase):
    pass

class RestaurantImageOut(RestaurantImageBase):
    id: int
    restaurant_id: str

    class Config:
        from_attributes = True

# --- Restaurant Schemas ---
class RestaurantBase(BaseModel):
    name: str
    cuisine: str
    address: str
    city: str
    state: str
    phone: str
    email: EmailStr
    description: Optional[str] = None
    opening_hours: Optional[str] = "09:00 AM - 10:00 PM"
    license_number: str
    license_status: str = "Active"  # 'Active', 'Suspended', 'Expired', 'Under Review'
    restaurant_status: str = "Open"  # 'Open', 'Temporarily Closed', 'Permanently Closed'

class RestaurantCreate(RestaurantBase):
    images: Optional[List[RestaurantImageCreate]] = []

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    description: Optional[str] = None
    opening_hours: Optional[str] = None
    license_number: Optional[str] = None
    license_status: Optional[str] = None
    restaurant_status: Optional[str] = None
    images: Optional[List[RestaurantImageCreate]] = None

class RestaurantOut(RestaurantBase):
    id: str
    safety_score: int
    safety_rating: str
    
    # Inspection History Fields
    last_inspection_date: Optional[date] = None
    inspection_result: Optional[str] = None
    inspection_score: Optional[int] = None
    previous_violations: Optional[int] = None
    latest_violation: Optional[str] = None
    violation_severity: Optional[str] = None
    
    # Complaint Data
    complaint_count: Optional[int] = None
    latest_complaint: Optional[str] = None
    complaint_status: Optional[str] = None
    
    approval_status: str
    owner_id: int
    created_at: datetime.datetime
    images: List[RestaurantImageOut] = []

    class Config:
        from_attributes = True
