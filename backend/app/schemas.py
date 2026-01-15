from pydantic import BaseModel
from typing import Optional, List


class PaperResponse(BaseModel):
    id: int
    title: str
    year: Optional[int]
    venue: Optional[str]
    citation_count: Optional[int]

    class Config:
        from_attributes = True


class FacultyResponse(BaseModel):
    id: int
    name: str
    affiliation: Optional[str]
    h_index: Optional[int]
    paper_count: Optional[int]
    semantic_scholar_id: Optional[str]

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    faculty: FacultyResponse
    similarity: float
    papers: list[PaperResponse] = []


class SearchRequest(BaseModel):
    query: str
    limit: int = 10
    min_h_index: int = 0
    universities: Optional[List[str]] = None

class ExplanationRequest(BaseModel):
    interests: str
    faculty_id: int


class ExplanationResponse(BaseModel):
    explanation: str


class CVUploadResponse(BaseModel):
    """Response for CV upload endpoint."""
    extracted_interests: str
    results: list[SearchResult]
