"""FastAPI backend for Trip Planner Agent.

Refactored to use centralized settings and expose diagnostic endpoints.
"""

from typing import Any, Dict, List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from trip_planner_agent import TripRequest, plan_trip

from backend.logging_config import configure_logging
from backend.settings import settings
from backend.version import __version__

load_dotenv()
configure_logging()

if settings.langfuse_public_key and settings.langfuse_secret_key:
    print("✅ Langfuse environment variables loaded successfully")
else:
    print("⚠️ Langfuse env vars not found; check .env")

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A LangGraph-based trip planning system",
    version=__version__,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripPlanRequest(BaseModel):
    """Request model for trip planning."""

    destination: str
    duration: int
    budget: float
    interests: List[str] = []
    start_date: str
    end_date: str
    accommodation_type: str = "hotel"
    transportation_type: str = "flight"


class TripPlanResponse(BaseModel):
    """Response model for trip planning."""

    success: bool
    data: Dict[str, Any] = None
    error: str = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Trip Planner Agent API is running!"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "trip-planner-agent",
        "version": __version__,
        "environment": settings.environment,
    }


@app.get("/version")
async def version():
    """Return service version only."""
    return {"version": __version__}


@app.get("/config")
async def config_snapshot():
    """Return non-sensitive configuration snapshot (secrets redacted)."""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "version": __version__,
        "openai_api_key": bool(settings.openai_api_key),
        "langfuse_public_key": bool(settings.langfuse_public_key),
        "langfuse_secret_key": bool(settings.langfuse_secret_key),
        "langfuse_host": settings.langfuse_host,
    }


@app.post("/plan-trip", response_model=TripPlanResponse)
async def create_trip_plan(request: TripPlanRequest):
    """Create a comprehensive trip plan"""
    try:
        # Validate API key
        if not settings.openai_api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")

        # Convert request to TripRequest
        trip_request = TripRequest(
            destination=request.destination,
            duration=request.duration,
            budget=request.budget,
            interests=request.interests,
            start_date=request.start_date,
            end_date=request.end_date,
            accommodation_type=request.accommodation_type,
            transportation_type=request.transportation_type,
        )

        # Generate trip plan
        result = plan_trip(trip_request)

        return TripPlanResponse(success=True, data=result)

    except ValueError as e:
        return TripPlanResponse(success=False, error=str(e))


@app.get("/destinations")
async def get_popular_destinations():
    """Get list of popular destinations"""
    destinations = [
        {"name": "Paris", "country": "France", "currency": "EUR"},
        {"name": "Tokyo", "country": "Japan", "currency": "JPY"},
        {"name": "New York", "country": "USA", "currency": "USD"},
        {"name": "London", "country": "UK", "currency": "GBP"},
        {"name": "Rome", "country": "Italy", "currency": "EUR"},
        {"name": "Barcelona", "country": "Spain", "currency": "EUR"},
        {"name": "Amsterdam", "country": "Netherlands", "currency": "EUR"},
        {"name": "Sydney", "country": "Australia", "currency": "AUD"},
        {"name": "Dubai", "country": "UAE", "currency": "AED"},
        {"name": "Bangkok", "country": "Thailand", "currency": "THB"},
    ]
    return {"destinations": destinations}


@app.get("/interests")
async def get_common_interests():
    """Get list of common travel interests"""
    interests = [
        "art",
        "history",
        "food",
        "nature",
        "adventure",
        "culture",
        "shopping",
        "nightlife",
        "beaches",
        "mountains",
        "museums",
        "architecture",
        "photography",
        "music",
        "sports",
        "wellness",
        "local experiences",
        "festivals",
        "wildlife",
        "hiking",
    ]
    return {"interests": interests}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
