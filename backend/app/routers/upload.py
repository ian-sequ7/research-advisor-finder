from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas import CVUploadResponse
from app.services.cv_parser import extract_text, summarize_research_interests
from app.services.embeddings import get_embedding
from app.services.search import search_faculty_by_embedding

router = APIRouter()


@router.post("/cv", response_model=CVUploadResponse)
async def upload_cv(
    file: UploadFile = File(...),
    limit: int = Query(default=10, ge=1, le=20),
    min_h_index: Optional[int] = Query(default=0, ge=0),
    universities: Optional[list[str]] = Query(default=None),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    filename_lower = file.filename.lower()
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported"
        )

    try:
        file_bytes = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")

    try:
        cv_text = extract_text(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

    if not cv_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text from file")

    try:
        interests_summary = summarize_research_interests(cv_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing CV: {str(e)}"
        )

    try:
        query_embedding = get_embedding(interests_summary)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating embedding: {str(e)}"
        )

    search_results = search_faculty_by_embedding(
        db=db,
        embedding=query_embedding,
        limit=limit,
        min_h_index=min_h_index,
        universities=universities,
    )

    return CVUploadResponse(
        extracted_interests=interests_summary,
        results=search_results
    )
