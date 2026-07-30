import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Date, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'customer', 'owner', 'admin'
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    restaurants = relationship("Restaurant", back_populates="owner", cascade="all, delete-orphan")

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(String, primary_key=True, index=True)  # R0001, R0002 etc.
    name = Column(String, nullable=False, index=True)
    cuisine = Column(String, nullable=False, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False, index=True)
    state = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    opening_hours = Column(String, nullable=True)
    license_number = Column(String, unique=True, index=True, nullable=False)
    license_status = Column(String, nullable=False)  # 'Active', 'Suspended', 'Expired', 'Under Review'
    restaurant_status = Column(String, nullable=False)  # 'Open', 'Temporarily Closed', 'Permanently Closed'
    safety_score = Column(Integer, nullable=False)  # 0 to 100
    safety_rating = Column(String, nullable=False)  # 'Excellent', 'Good', 'Fair', 'Poor'
    
    # Inspection History Fields
    last_inspection_date = Column(Date, nullable=True)
    inspection_result = Column(String, nullable=True)  # 'Passed', 'Passed with Violations', 'Failed'
    inspection_score = Column(Integer, nullable=True)  # 0 to 100
    previous_violations = Column(Integer, default=0)
    latest_violation = Column(String, nullable=True)
    violation_severity = Column(String, nullable=True)  # 'Critical', 'Major', 'Minor'
    
    # Complaint Data
    complaint_count = Column(Integer, default=0)
    latest_complaint = Column(String, nullable=True)
    complaint_status = Column(String, nullable=True)  # 'Verified', 'Rejected', 'Under Investigation'
    
    approval_status = Column(String, default="Pending", index=True, nullable=False)  # 'Pending', 'Approved', 'Rejected'
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="restaurants")
    images = relationship("RestaurantImage", back_populates="restaurant", cascade="all, delete-orphan")
    inspections = relationship("Inspection", back_populates="restaurant", cascade="all, delete-orphan")
    complaints = relationship("Complaint", back_populates="restaurant", cascade="all, delete-orphan")

class RestaurantImage(Base):
    __tablename__ = "restaurant_images"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(String, ForeignKey("restaurants.id"), nullable=False)
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="images")


class Inspector(Base):
    __tablename__ = "inspectors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    badge_number = Column(String, unique=True, nullable=False)
    certification_level = Column(String, nullable=False)  # 'Senior', 'Junior', 'Lead'
    department = Column(String, nullable=False)
    contact_email = Column(String, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    inspections = relationship("Inspection", back_populates="inspector")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(String, ForeignKey("restaurants.id"), nullable=False)
    inspector_id = Column(Integer, ForeignKey("inspectors.id"), nullable=False)
    
    # Inspection Details
    inspection_date = Column(Date, nullable=False)
    inspection_type = Column(String, nullable=False)  # 'Routine', 'Follow-up', 'Complaint-based', 'Pre-opening'
    inspection_duration_minutes = Column(Integer, nullable=True)
    
    # Scoring
    total_score = Column(Integer, nullable=False)  # 0-100
    pass_fail_status = Column(String, nullable=False)  # 'Passed', 'Passed with Violations', 'Failed'
    
    # Risk Assessment
    risk_level = Column(String, nullable=False)  # 'Low', 'Medium', 'High', 'Critical'
    
    # Administrative
    permit_action = Column(String, nullable=True)  # 'None', 'Suspended', 'Revoked', 'Warning Issued'
    reinspection_required = Column(Boolean, default=False)
    reinspection_deadline = Column(Date, nullable=True)
    
    # Notes and Comments
    inspector_notes = Column(Text, nullable=True)
    corrective_actions_required = Column(Text, nullable=True)
    
    # Compliance
    previous_violations_corrected = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="inspections")
    inspector = relationship("Inspector", back_populates="inspections")
    violations = relationship("Violation", back_populates="inspection", cascade="all, delete-orphan")
    photos = relationship("InspectionPhoto", back_populates="inspection", cascade="all, delete-orphan")


class ViolationCode(Base):
    __tablename__ = "violation_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)  # e.g., "2-102.11", "3-301.11"
    category = Column(String, nullable=False)  # 'Food Source', 'Equipment', 'Personnel', etc.
    description = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # 'Critical', 'Major', 'Minor'
    points_deducted = Column(Integer, default=0)
    
    # Risk information
    health_risk_level = Column(String, nullable=False)  # 'High', 'Medium', 'Low'
    typical_corrective_action = Column(Text, nullable=True)
    
    # Relationships
    violations = relationship("Violation", back_populates="violation_code")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    violation_code_id = Column(Integer, ForeignKey("violation_codes.id"), nullable=False)
    
    # Violation Details
    description = Column(Text, nullable=False)  # Specific description of what was found
    location_in_restaurant = Column(String, nullable=True)  # 'Kitchen', 'Storage Area', 'Dining Room', etc.
    
    # Severity and Impact
    severity_level = Column(String, nullable=False)  # 'Critical', 'Major', 'Minor'
    points_deducted = Column(Integer, default=0)
    
    # Status Tracking
    corrected_on_site = Column(Boolean, default=False)
    correction_deadline = Column(Date, nullable=True)
    corrected_date = Column(Date, nullable=True)
    verified_corrected = Column(Boolean, default=False)
    
    # Additional Details
    repeat_violation = Column(Boolean, default=False)  # Has this violation occurred before?
    management_response = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    inspection = relationship("Inspection", back_populates="violations")
    violation_code = relationship("ViolationCode", back_populates="violations")
    photos = relationship("ViolationPhoto", back_populates="violation", cascade="all, delete-orphan")


class InspectionPhoto(Base):
    __tablename__ = "inspection_photos"

    id = Column(Integer, primary_key=True, index=True)
    inspection_id = Column(Integer, ForeignKey("inspections.id"), nullable=False)
    
    photo_url = Column(String, nullable=False)
    caption = Column(String, nullable=True)
    photo_type = Column(String, nullable=False)  # 'General', 'Equipment', 'Storage', 'Cleanliness'
    taken_by = Column(String, nullable=True)  # Inspector name
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    inspection = relationship("Inspection", back_populates="photos")


class ViolationPhoto(Base):
    __tablename__ = "violation_photos"

    id = Column(Integer, primary_key=True, index=True)
    violation_id = Column(Integer, ForeignKey("violations.id"), nullable=False)
    
    photo_url = Column(String, nullable=False)
    caption = Column(String, nullable=True)
    shows_before_after = Column(String, nullable=False)  # 'Before', 'After', 'During'
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    violation = relationship("Violation", back_populates="photos")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(String, ForeignKey("restaurants.id"), nullable=False)
    
    # Complaint Details
    complaint_type = Column(String, nullable=False)  # 'Food Safety', 'Service', 'Cleanliness', 'Other'
    description = Column(Text, nullable=False)
    complainant_name = Column(String, nullable=True)  # Optional anonymous
    complainant_contact = Column(String, nullable=True)
    
    # Status Tracking
    status = Column(String, default="Submitted")  # 'Submitted', 'Under Investigation', 'Verified', 'Rejected', 'Resolved'
    priority_level = Column(String, default="Medium")  # 'Low', 'Medium', 'High', 'Critical'
    
    # Investigation
    assigned_inspector_id = Column(Integer, ForeignKey("inspectors.id"), nullable=True)
    investigation_notes = Column(Text, nullable=True)
    resolution_details = Column(Text, nullable=True)
    
    # Dates
    complaint_date = Column(Date, nullable=False)
    investigation_date = Column(Date, nullable=True)
    resolution_date = Column(Date, nullable=True)
    
    # Follow-up
    follow_up_inspection_required = Column(Boolean, default=False)
    follow_up_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    restaurant = relationship("Restaurant", back_populates="complaints")
    assigned_inspector = relationship("Inspector", foreign_keys=[assigned_inspector_id])


# Update Restaurant model to include new relationships
