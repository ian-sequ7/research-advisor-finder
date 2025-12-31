import sys
sys.path.insert(0, '/app')

import os
from openai import OpenAI
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Faculty, Paper

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def build_faculty_text(faculty: Faculty, papers: list[Paper]) -> str:
    """Build text representation of faculty for embedding."""
    parts = [f"Professor {faculty.name}"]
    
    if faculty.affiliation:
        parts.append(f"at {faculty.affiliation}")
    
    if papers:
        parts.append("\nResearch papers:")
        for paper in papers[:10]:  # Top 10 papers
            parts.append(f"- {paper.title}")
            if paper.abstract:
                # Truncate long abstracts
                abstract = paper.abstract[:500]
                parts.append(f"  {abstract}")
    
    return "\n".join(parts)
