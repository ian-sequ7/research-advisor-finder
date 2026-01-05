from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models
from app.routers import search

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Research Advisor Finder API",
    description="Find faculty with similar research interests",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://research-advisor-frontend.vercel.app",
        "https://research-advisor-frontend-ians-projects-ac3260d9.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search.router, prefix="/api/search", tags=["search"])

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
