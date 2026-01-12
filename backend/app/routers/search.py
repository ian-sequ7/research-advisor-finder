from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.services.explanations import generate_explanation
from app.schemas import ExplanationRequest, ExplanationResponse
from app.schemas import SearchRequest, SearchResult
from app.services.embeddings import get_embedding
from app.models import Faculty, Paper

router = APIRouter()

@router.post("/", response_model=list[SearchResult])
def search_faculty(request: SearchRequest, db: Session = Depends(get_db)):

    query_embedding = get_embedding(request.query)

    where_clauses = ["embedding IS NOT NULL", "h_index >= :min_h"]
    params = {
        "embedding": str(query_embedding),
        "min_h": request.min_h_index,
        "limit": request.limit
    }

    if request.universities:
        where_clauses.append("affiliation = ANY(:universities)")
        params["universities"] = request.universities

    where_sql = " AND ".join(where_clauses)

    results = db.execute(
        text(f"""
            SELECT
                id, name, affiliation, h_index, paper_count,
                semantic_scholar_id,
                1 - (embedding <=> :embedding) as similarity
            FROM faculty
            WHERE {where_sql}
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """),
        params
    ).fetchall()


    search_results = []
    for row in results:
        papers = db.query(Paper).filter(
            Paper.faculty_id == row.id
        ).order_by(Paper.citation_count.desc()).limit(5).all()
        
        search_results.append(SearchResult(
            faculty={
                "id": row.id,
                "name": row.name,
                "affiliation": row.affiliation,
                "h_index": row.h_index,
                "paper_count": row.paper_count,
                "semantic_scholar_id": row.semantic_scholar_id,
            },
            similarity=float(row.similarity),
            papers=[{
                "id": p.id,
                "title": p.title,
                "year": p.year,
                "venue": p.venue,
                "citation_count": p.citation_count
            } for p in papers]
        ))
    return search_results

@router.post("/explain", response_model=ExplanationResponse)
def explain_match(request: ExplanationRequest, db: Session = Depends(get_db)):
    """Generate explanation for why a faculty member matches."""
    faculty = db.query(Faculty).filter(Faculty.id == request.faculty_id).first()
    if not faculty:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Faculty not found")
    
    papers = db.query(Paper).filter(
        Paper.faculty_id == faculty.id
    ).order_by(Paper.citation_count.desc()).limit(5).all()
    
    paper_titles = [p.title for p in papers]
    
    explanation = generate_explanation(
        request.interests,
        faculty.name,
        paper_titles
    )
    
    return ExplanationResponse(explanation=explanation)
