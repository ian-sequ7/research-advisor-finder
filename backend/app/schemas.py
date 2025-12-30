from pydantic import BaseModel
from typing import Optional

class PaperRespose(BaseModel):
    id: int
    title: str
    year: Optional[int]
    venue: Optional[str]
    citation_count: Optional[int]   
