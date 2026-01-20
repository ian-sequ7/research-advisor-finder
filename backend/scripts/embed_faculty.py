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
    parts = [f"Professor {faculty.name}"]

    if faculty.affiliation:
        parts.append(f"at {faculty.affiliation}")

    if papers:
        parts.append("\nResearch papers:")
        for paper in papers[:10]:
            parts.append(f"- {paper.title}")
            if paper.abstract:
                abstract = paper.abstract[:500]
                parts.append(f"  {abstract}")

    return "\n".join(parts)

def embed_all_faculty():
    db = SessionLocal()

    try:
        faculty_list = db.query(Faculty).filter(
            Faculty.embedding.is_(None)
        ).all()

        print(f"Found {len(faculty_list)} faculty to embed")

        for faculty in faculty_list:
            print(f"Embedding: {faculty.name}")

            papers = db.query(Paper).filter(
                Paper.faculty_id == faculty.id
            ).order_by(Paper.citation_count.desc()).limit(10).all()

            text = build_faculty_text(faculty, papers)
            embedding = get_embedding(text)

            faculty.embedding = embedding
            db.commit()

            print(f"  Done ({len(embedding)} dimensions)")

        print("\nAll embeddings generated!")

    finally:
        db.close()


if __name__ == "__main__":
    embed_all_faculty()
