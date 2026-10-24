import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
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
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime.datetime

# --- Restaurant Image Schemas ---
class RestaurantImageBase(BaseModel):
    image_url: str
    is_primary: bool = False

class RestaurantImageCreate(RestaurantImageBase):
    pass

class RestaurantImageOut(RestaurantImageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    restaurant_id: str

# --- Explainable Assessment Schema ---
class FoodSafetyAssessmentOut(BaseModel):
    safety_score: int
    safety_rating: str  # 'Excellent', 'Good', 'Needs Improvement', 'High Risk'
    grade_label: str    # 'Pass / Excellent', 'Good / Low Risk', 'Needs Improvement', 'High Risk / Alert', 'Uninspected / Pending', 'Stale Data Warning'
    risk_level: str     # 'Low', 'Medium', 'High', 'Critical'
    confidence_score: float
    data_freshness_status: str  # 'Current', 'Stale', 'Expired', 'Unknown'
    days_since_inspection: Optional[int] = None
    critical_violations_count: int = 0
    non_critical_violations_count: int = 0
    repeat_violations_count: int = 0
    active_complaints_count: int = 0
    risk_factors: List[str] = []
    positive_factors: List[str] = []
    summary_explanation: str
    consumer_advice: str
    provenance_disclaimer: str

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

    # Provenance fields
    source_name: Optional[str] = "SafeBite Synthetic Benchmark"
    source_url: Optional[str] = None
    source_record_id: Optional[str] = None
    verification_status: Optional[str] = "Synthetic Demonstration"
    confidence_score: Optional[float] = 0.75
    is_synthetic: bool = True
    data_freshness_status: Optional[str] = "Current"

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
    model_config = ConfigDict(from_attributes=True)

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
    last_synced_at: Optional[datetime.datetime] = None
    images: List[RestaurantImageOut] = []

    # Optional dynamic assessment attached on detail queries
    assessment: Optional[FoodSafetyAssessmentOut] = None

# --- Correction Request Schemas ---
class CorrectionRequestCreate(BaseModel):
    restaurant_id: str
    inspection_id: Optional[int] = None
    request_type: str  # 'Data Correction', 'Inspection Dispute', 'License Update'
    details: str
    evidence_url: Optional[str] = None

class CorrectionRequestReview(BaseModel):
    status: str  # 'Approved', 'Rejected'
    admin_notes: Optional[str] = None

class CorrectionRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: str
    inspection_id: Optional[int] = None
    owner_id: int
    request_type: str
    details: str
    evidence_url: Optional[str] = None
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime.datetime
    reviewed_at: Optional[datetime.datetime] = None

# --- Restaurant Match (For Extension and Delivery Companion) ---
class RestaurantMatchRequest(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    platform: Optional[str] = "generic"  # 'swiggy', 'zomato', 'companion_demo'

class RestaurantMatchResponse(BaseModel):
    matched: bool
    match_confidence: float
    restaurant: Optional[RestaurantOut] = None
    assessment: Optional[FoodSafetyAssessmentOut] = None
    source_attribution: Optional[str] = None
    notice: Optional[str] = None
