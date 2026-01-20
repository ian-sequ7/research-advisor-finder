import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import engine, Base
from app import models
from app.routers import search, upload, explore

Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])

app = FastAPI(
    title="Research Advisor Finder API",
    description="Find faculty with similar research interests",
    version="1.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "https://research-advisor-frontend.vercel.app",
        os.environ.get("FRONTEND_URL", "http://localhost:3000"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(explore.router, prefix="/api/explore", tags=["explore"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def root():
    return {
        "message": "Research Advisor Finder API",
        "docs": "/docs",
        "health": "/health"
    }
