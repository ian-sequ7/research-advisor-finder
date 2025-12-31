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

