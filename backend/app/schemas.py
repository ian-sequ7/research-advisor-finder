from pydantic import BaseModel
from typing import Optional


    # how a paper is seen from front
class PaperRespose(BaseModel):
    id: int
    title: str
    year: Optional[int]
    venue: Optional[str]
    citation_count: Optional[int]  

    class Config:
        from_attributes =True

class FacultyResponse(BaseModel):
    id: int
    name: str
    affiliation: Optional[str]
    h_index: Optional[int]
    paper_count: Optional[int]
    semantic_scholar_id: optional[int]

    class Config
        from_attributes = True

class SearchResult(BaseModel):
    faculty: FacultyResponse
    similarity: float # similarity basically means a higher # means a better match
    papers: list[PaperResponse] = []
    
class SearchRequest(Basemodel):
    query: str
    limit: int = 10
    min_h_index: int = 0

class ExplanationRequest(BaseModel):
    interests: str
    faculty_id: str

class ExplanationResponse(BaseModel):
    explanation: str
