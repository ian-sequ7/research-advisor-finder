from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.schemas import ExplanationRequest, ExplanationResponse, SearchRequest, SearchResult
from app.services.embeddings import get_embedding
from app.services.explanations import generate_explanation
from app.services.query_expansion import expand_query
from app.services.search import search_faculty_hybrid
from app.models import Faculty, Paper

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/", response_model=list[SearchResult])
@limiter.limit("30/minute")
def search_faculty(req: Request, request: SearchRequest, db: Session = Depends(get_db)):
    # Expand query to include full terms for common abbreviations
    expanded_query = expand_query(request.query)
    query_embedding = get_embedding(expanded_query)
    return search_faculty_hybrid(
        db=db,
        query=expanded_query,
        embedding=query_embedding,
        limit=request.limit,
        min_h_index=request.min_h_index,
        universities=request.universities,
    )

@router.post("/explain", response_model=ExplanationResponse)
@limiter.limit("20/minute")
def explain_match(req: Request, request: ExplanationRequest, db: Session = Depends(get_db)):
    faculty = db.query(Faculty).filter(Faculty.id == request.faculty_id).first()
    if not faculty:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Faculty not found")

    papers = db.query(Paper).filter(
        Paper.faculty_id == faculty.id
    ).order_by(Paper.citation_count.desc()).limit(5).all()

    paper_titles = [p.title for p in papers]

    result = generate_explanation(
        request.interests,
        faculty.name,
        paper_titles
    )

    return ExplanationResponse(
        explanation=result["explanation"],
        breakdown=result.get("breakdown")
    )
