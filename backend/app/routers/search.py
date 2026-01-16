from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import ExplanationRequest, ExplanationResponse, SearchRequest, SearchResult
from app.services.embeddings import get_embedding
from app.services.explanations import generate_explanation
from app.services.search import search_faculty_by_embedding
from app.models import Faculty, Paper

router = APIRouter()

@router.post("/", response_model=list[SearchResult])
def search_faculty(request: SearchRequest, db: Session = Depends(get_db)):
    query_embedding = get_embedding(request.query)
    return search_faculty_by_embedding(
        db=db,
        embedding=query_embedding,
        limit=request.limit,
        min_h_index=request.min_h_index,
        universities=request.universities,
    )

@router.post("/explain", response_model=ExplanationResponse)
def explain_match(request: ExplanationRequest, db: Session = Depends(get_db)):
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
