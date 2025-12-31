from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db
from app.schemas import SearchRequest, SearchResult
from app.services.embeddings import get_embedding
from app.models import Faculty, Paper

router = APIRouter()

@router.post("/", response_model=list[SearchResult])
def search_faculty(request: SearchRequest, db: Session = Depends(get_db)):

    query_embedding = get_embedding(request.query)

    results = db.execute(
        text("""
            SELECT 
                id, name, affiliation, h_index, paper_count,
                semantic_scholar_id,
                1 - (embedding <=> :embedding) as similarity
            FROM faculty
            WHERE embedding IS NOT NULL
            AND h_index >= :min_h
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """),
        {
            "embedding": str(query_embedding),
            "min_h": request.min_h_index,
            "limit": request.limit
        }
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
