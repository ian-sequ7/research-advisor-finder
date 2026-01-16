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
    research_tags: list[str] = []

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


class BreakdownItem(BaseModel):
    level: str  # High, Medium, Low
    reason: str


class ExplanationBreakdown(BaseModel):
    topic_alignment: Optional[BreakdownItem] = None
    paper_relevance: Optional[BreakdownItem] = None
    research_fit: Optional[BreakdownItem] = None


class ExplanationResponse(BaseModel):
    explanation: str
    breakdown: Optional[ExplanationBreakdown] = None


class CVUploadResponse(BaseModel):
    """Response for CV upload endpoint."""
    extracted_interests: str
    results: list[SearchResult]


# ============== Explore (Research Path Explorer) ==============

class ExplorePaper(BaseModel):
    """Paper shown during exploration."""
    id: int
    title: str
    abstract: Optional[str]
    year: Optional[int]
    venue: Optional[str]
    faculty_name: Optional[str] = None

    class Config:
        from_attributes = True


class ExploreStartRequest(BaseModel):
    """Request to start exploration session."""
    initial_interest: str


class ExploreStartResponse(BaseModel):
    """Response with session ID and initial papers."""
    session_id: str
    papers: list[ExplorePaper]
    prompt: str


class ExploreRespondRequest(BaseModel):
    """User's response during exploration."""
    session_id: str
    response: str


class ExploreRespondResponse(BaseModel):
    """Next set of papers based on user response."""
    papers: list[ExplorePaper]
    prompt: str
    is_ready: bool  # True if system detects convergence


class ExploreFinishRequest(BaseModel):
    """Request to finish exploration and get results."""
    session_id: str


class FacultyMatch(BaseModel):
    """Faculty match with explanation."""
    faculty: FacultyResponse
    similarity: float
    explanation: str
    key_paper: Optional[str] = None


class ExploreFinishResponse(BaseModel):
    """Final exploration results."""
    direction_summary: str
    direction_description: str
    faculty_matches: list[FacultyMatch]
