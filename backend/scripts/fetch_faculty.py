"""
Fetch faculty data from Semantic Scholar API using curated list.
Run this to populate the database with faculty from top 10 CS programs.
"""
import requests
import time
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Faculty, Paper

S2_API = "https://api.semanticscholar.org/graph/v1"

FACULTY_BY_SCHOOL = {
    "MIT": [
        "Antonio Torralba", "Aleksander Madry", "Daniela Rus", "Tomás Lozano-Pérez",
        "Leslie Kaelbling", "Joshua Tenenbaum", "Regina Barzilay", "Pulkit Agrawal",
        "Samuel Madden", "Srini Devadas", "Armando Solar-Lezama", "Manolis Kellis",
        "Dina Katabi", "Wojciech Matusik", "Ankur Moitra"
    ],
    "Stanford": [
        "Christopher Manning", "Percy Liang", "Fei-Fei Li", "Chelsea Finn",
        "Dorsa Sadigh", "Christopher Ré", "Jure Leskovec", "Dan Jurafsky",
        "Tengyu Ma", "Stefano Ermon", "Monica Lam", "John Mitchell",
        "Leonidas Guibas", "Jeannette Bohg", "Diyi Yang"
    ],
    "CMU": [
        "Tom Mitchell", "Ruslan Salakhutdinov", "Zico Kolter", "Graham Neubig",
        "Yonatan Bisk", "Katerina Fragkiadaki", "Barnabás Póczos", "Jeff Schneider",
        "Emma Brunskill", "Abhinav Gupta", "Srinivas Narasimhan", "Martial Hebert",
        "Manuel Blum", "David Andersen", "Virginia Smith"
    ],
    "UC Berkeley": [
        "Pieter Abbeel", "Trevor Darrell", "Sergey Levine", "Dawn Song",
        "Stuart Russell", "Michael Jordan", "Ion Stoica", "Joseph Gonzalez",
        "Jitendra Malik", "Alexei Efros", "Ken Goldberg", "Anca Dragan",
        "Alison Gopnik", "Raluca Ada Popa", "Moritz Hardt"
    ],
    "UIUC": [
        "Jiawei Han", "ChengXiang Zhai", "Dan Roth", "Julia Hockenmaier",
        "Svetlana Lazebnik", "David Forsyth", "Derek Hoiem", "Saurabh Sinha",
        "Tandy Warnow", "Sanjay Kale", "Karrie Karahalios", "Ranjitha Kumar",
        "Charith Mendis", "Yuxiong Wang", "Heng Ji"
    ],
    "Cornell": [
        "Thorsten Joachims", "Kilian Weinberger", "Carla Gomes", "Bart Selman",
        "Ashutosh Saxena", "Noah Snavely", "Serge Belongie", "Kavita Bala",
        "Ross Tate", "Eva Tardos", "Jon Kleinberg", "Robert Kleinberg",
        "Yoav Artzi", "Sasha Rush", "Chris De Sa"
    ],
    "UW": [
        "Luke Zettlemoyer", "Noah Smith", "Yejin Choi", "Ali Farhadi",
        "Carlos Guestrin", "Shyam Gollakota", "Ira Kemelmacher-Shlizerman", "Dieter Fox",
        "Sham Kakade", "Sewoong Oh", "Su-In Lee", "Hannaneh Hajishirzi",
        "Ranjay Krishna", "Adriana Schulz", "Zaid Harchaoui"
    ],
    "Georgia Tech": [
        "Devi Parikh", "Dhruv Batra", "James Rehg", "Irfan Essa",
        "Byron Boots", "Sonia Chernova", "Mark Riedl", "Charles Isbell",
        "Polo Chau", "Le Song", "Judy Hoffman", "Zsolt Kira",
        "Hao-Tsung Yang", "Matthew Gombolay", "Danfei Xu"
    ],
    "Princeton": [
        "Sanjeev Arora", "Elad Hazan", "Karthik Narasimhan", "Danqi Chen",
        "Jia Deng", "Olga Russakovsky", "Ryan Adams", "Tom Griffiths",
        "Sebastian Seung", "Barbara Engelhardt", "Kai Li", "Jennifer Rexford",
        "Aarti Gupta", "Adji Bousso Dieng", "Chi Jin"
    ],
    "UT Austin": [
        "Peter Stone", "Scott Niekum", "Raymond Mooney", "Kristen Grauman",
        "Philipp Krähenbühl", "Qixing Huang", "Greg Durrett", "Jessy Li",
        "Yuke Zhu", "Chandrajit Bajaj", "William Hwang", "Roberto Martín-Martín",
        "Amy Zhang", "Swarat Chaudhuri", "Isil Dillig"
    ]
}


def search_author(name: str) -> dict | None:
    url = f"{S2_API}/author/search"
    params = {"query": name, "limit": 1}
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("data"):
            return data["data"][0]
    except Exception as e:
        print(f"  Error: {e}")
    return None


def get_author_details(author_id: str) -> dict | None:
    url = f"{S2_API}/author/{author_id}"
    params = {
        "fields": "name,affiliations,homepage,hIndex,citationCount,paperCount,papers.title,papers.year,papers.abstract,papers.venue,papers.citationCount"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  Error: {e}")
    return None


def save_faculty(db: Session, author: dict, school: str) -> Faculty | None:
    existing = db.query(Faculty).filter(
        Faculty.semantic_scholar_id == author["authorId"]
    ).first()
    
    if existing:
        print(f"  Already exists, skipping")
        return existing
    
    faculty = Faculty(
        semantic_scholar_id=author["authorId"],
        name=author["name"],
        affiliation=school,
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
    print(f"  Saved {author['name']} ({school}) with {min(len(papers_sorted), 20)} papers")
    return faculty


def fetch_all_faculty():
    db = SessionLocal()
    total_count = sum(len(f) for f in FACULTY_BY_SCHOOL.values())
    processed = 0
    saved = 0
    failed = 0
    
    try:
        for school, faculty_list in FACULTY_BY_SCHOOL.items():
            print(f"\nProcessing: {school} ({len(faculty_list)} faculty)")
            
            for name in faculty_list:
                processed += 1
                print(f"[{processed}/{total_count}] {name}")
                
                search_result = search_author(name)
                if not search_result:
                    print(f"  Not found")
                    failed += 1
                    time.sleep(3)
                    continue
                
                author = get_author_details(search_result["authorId"])
                if not author:
                    failed += 1
                    time.sleep(3)
                    continue
                
                result = save_faculty(db, author, school)
                if result:
                    saved += 1
                
                time.sleep(3)
        
        print(f"\nDONE! Processed: {processed}, Saved: {saved}, Failed: {failed}")
        
    finally:
        db.close()


if __name__ == "__main__":
    fetch_all_faculty()
