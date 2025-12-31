import sys
sys.path.insert(0, 'app')

import requests
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Faculty, Paper

S2_API = "https://api.semanticscholar.org/graph/v1"

SEED_FACULTY = [
    "Geoffrey Hinton",
    "Yann LeCun",
    "Yoshua Bengio",
    "Fei-Fei Li",
    "Andrew Ng",
    "Demis Hassabis",
    "Ilya Sutskever",
    "Andrej Karpathy",
    "Chris Manning",
    "Michael I. Jordan",
]

def search_author(name: str) -> dict | None:
    """Search for an author by name."""
    url = f"{S2_API}/author/search"
    params = {"query": name, "limit": 1}

    try:
        resp = requests.get(url, params=params, timeout = 10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("data"):
            return data["data"][0]
    except Exception as e:
        print(f" Error searching for {name}: {e}")
    return None

def get_author_details(author_id: str) -> dict | None:
    """Get detailed author info including papers."""
    url = f"{S2_API}/author/{author_id}"
    params = {
        "fields": "name,affiliations,homepage,hIndex,citationCount,paperCount,papers.title,papers.year,papers.abstract,papers.venue,papers.citationCount"
    }
    
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Error getting details for {author_id}: {e}")
    return None

def save_faculty(db: Session, author: dict) -> Faculty | None:
    existing = db.query(Faculty).filter(
        Faculty.semantic_scholar_id == author["authorID"]
    ).first()

    if existing:
        print(f" {author['name']} already exists, skipping")
        return existing

    faculty = Faculty(
        semantic_scholar_id=author["authorId"],
        name=author["name"],
        affiliation=author.get("affiliations", [None])[0] if author.get("affiliations") else None,
        homepage=author.get("homepage"),
        h_index=author.get("hIndex"),
        citation_count=author.get("citationCount"),
        paper_count=author.get("paperCount"),
    )
    db.add(faculty)
    db.flush()

    papers = author.get("papers", [])
    papers_with_citations = [p for p in papers if p.get("citationCount") is not None]
    papers_sorted = sorted(papers_with_citations, key=lambda x: x["citationCount"], reverse=True)

    for paper_data in papers_sorted[:20]:
        paper = Paper(
            faculty_id=faculty.id,
            title=paper_data.get("title", "Untitled"),
            abstract=paper_data.get("abstract"),
            year=paper_data.get("year"),
            venue=paper_data.get("venue"),
            citation_count=paper_data.get("citationCount"),
        )
        db.add(paper)
    db.commit()
    print(f" Saved {author['name']} with {min(len(papers_sorted), 20)} papers")
    return faculty

def fetch_all_faculty():
    db = SessionLocal()

    try:
        for name in SEED_FACULTY:
            print(f"Processing: {name}")

            search_result = search_author(name)
            if not search_result:
                print(f" Not Found: {name}")
                continue

            author = get_author_details(search_result["authorId"])
            if not author:
                continue

            save_faculty(db, author)
            time.sleep(1)

        print("\nDone! Faculty data fetched")
    finally:
        db.close()

if __name__ = "__main__":
    fetch_all_faculty()

