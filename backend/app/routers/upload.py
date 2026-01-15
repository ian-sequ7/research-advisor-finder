"""CV upload and matching endpoint."""
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional

from app.database import get_db
from app.schemas import SearchResult, CVUploadResponse
from app.services.cv_parser import extract_text, summarize_research_interests
from app.services.embeddings import get_embedding
from app.models import Paper

router = APIRouter()


@router.post("/cv", response_model=CVUploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    limit: int = Query(default=10, ge=1, le=20),
    min_h_index: Optional[int] = Query(default=0, ge=0),
    universities: Optional[list[str]] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    Upload a CV/resume (PDF or DOCX) and find matching faculty advisors.

    1. Extracts text from the uploaded file
    2. Uses Claude to summarize research interests
    3. Embeds the summary
    4. Matches against faculty embeddings
    """
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    filename_lower = file.filename.lower()
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    # Read file content
    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    # Extract text
    try:
        cv_text = extract_text(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    # Summarize research interests with Claude
    try:
        interests_summary = summarize_research_interests(cv_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing CV: {str(e)}"
        )

    # Generate embedding for the interests summary
    try:
        query_embedding = get_embedding(interests_summary)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating embedding: {str(e)}"
        )

    # Search for matching faculty (reusing search logic pattern)
    where_clauses = ["embedding IS NOT NULL", "h_index >= :min_h"]
    params = {
        "embedding": str(query_embedding),
        "min_h": min_h_index,
        "limit": limit
    }

    if universities:
        where_clauses.append("affiliation = ANY(:universities)")
        params["universities"] = universities

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

    # Build response with top papers
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

    return CVUploadResponse(
        extracted_interests=interests_summary,
        results=search_results
    )
