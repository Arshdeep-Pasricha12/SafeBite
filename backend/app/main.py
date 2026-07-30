from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, engine, get_db
from app.api import auth, restaurants, admin, inspections
from app.api.auth import get_current_user
from app.models.models import User
from app.schemas.schemas import UserOut

# Initialize FastAPI App
app = FastAPI(
    title="SafeBite API",
    description="Restaurant Discovery & Transparency Platform API",
    version="1.0.0"
)

# Set up CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev prototyping, allow all origins. Can be restricted in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup Table Creation (as a fallback/safety measure)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(auth.users_router, prefix="/api")
app.include_router(restaurants.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(inspections.router, prefix="/api")

# Support GET /profile alias directly under /api as per specification
@app.get("/api/profile", response_model=UserOut, tags=["users"])
def get_profile_alias(current_user: User = Depends(get_current_user)):
    """
    Alias route for GET /profile directly as requested in the specification.
    """
    return current_user

@app.get("/", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "app": "SafeBite",
        "version": "1.0.0 (Review 1 MVP)"
    }
