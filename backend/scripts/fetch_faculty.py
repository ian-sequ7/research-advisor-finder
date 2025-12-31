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




