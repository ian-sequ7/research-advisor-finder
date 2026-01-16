from pydantic import BaseModel, Field
from typing import Optional, List
import uuid


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
    level: str
    reason: str


class ExplanationBreakdown(BaseModel):
    topic_alignment: Optional[BreakdownItem] = None
    paper_relevance: Optional[BreakdownItem] = None
    research_fit: Optional[BreakdownItem] = None


class ExplanationResponse(BaseModel):
    explanation: str
    breakdown: Optional[ExplanationBreakdown] = None


class CVUploadResponse(BaseModel):
    extracted_interests: str
    results: list[SearchResult]


class ExplorePaper(BaseModel):
    id: int
    title: str
    abstract: Optional[str]
    year: Optional[int]
    venue: Optional[str]
    faculty_name: Optional[str] = None

    class Config:
        from_attributes = True


class ExploreStartRequest(BaseModel):
    initial_interest: str = Field(min_length=3, max_length=500)


class ExploreStartResponse(BaseModel):
    session_id: str
    papers: list[ExplorePaper]
    prompt: str


class ExploreRespondRequest(BaseModel):
    session_id: str = Field(pattern=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    response: str = Field(min_length=1, max_length=2000)


class ExploreRespondResponse(BaseModel):
    papers: list[ExplorePaper]
    prompt: str
    is_ready: bool


class ExploreFinishRequest(BaseModel):
    session_id: str


class FacultyMatch(BaseModel):
    faculty: FacultyResponse
    similarity: float
    explanation: str
    key_paper: Optional[str] = None


class ExploreFinishResponse(BaseModel):
    direction_summary: str
    direction_description: str
    faculty_matches: list[FacultyMatch]
