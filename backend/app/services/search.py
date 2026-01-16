from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Paper
from app.schemas import SearchResult


def search_faculty_by_embedding(
    db: Session,
    embedding: list[float],
    limit: int = 10,
    min_h_index: int = 0,
    universities: list[str] | None = None,
) -> list[SearchResult]:
    """
    Search faculty by embedding vector similarity and return results with top papers.
    Optimized to avoid N+1 queries by batch-fetching papers.
    """
    where_clauses = ["embedding IS NOT NULL", "h_index >= :min_h"]
    params = {
        "embedding": str(embedding),
        "min_h": min_h_index,
        "limit": limit
    }

    if universities:
        where_clauses.append("affiliation = ANY(:universities)")
        params["universities"] = universities

    where_sql = " AND ".join(where_clauses)

    results = db.execute(
        text(f"""
            SELECT
                id, name, affiliation, h_index, paper_count,
                semantic_scholar_id, research_tags,
                1 - (embedding <=> :embedding) as similarity
            FROM faculty
            WHERE {where_sql}
            ORDER BY embedding <=> :embedding
            LIMIT :limit
        """),
        params
    ).fetchall()

    if not results:
        return []

    faculty_ids = [row.id for row in results]

    # Batch fetch papers for all faculty (solves N+1 query problem)
    papers_query = (
        db.query(Paper)
        .filter(Paper.faculty_id.in_(faculty_ids))
        .order_by(Paper.citation_count.desc())
        .all()
    )

    # Group papers by faculty_id, keeping top 5 per faculty
    papers_by_faculty = {}
    for paper in papers_query:
        if paper.faculty_id not in papers_by_faculty:
            papers_by_faculty[paper.faculty_id] = []
        if len(papers_by_faculty[paper.faculty_id]) < 5:
            papers_by_faculty[paper.faculty_id].append(paper)

    # Build response
    search_results = []
    for row in results:
        papers = papers_by_faculty.get(row.id, [])

        search_results.append(SearchResult(
            faculty={
                "id": row.id,
                "name": row.name,
                "affiliation": row.affiliation,
                "h_index": row.h_index,
                "paper_count": row.paper_count,
                "semantic_scholar_id": row.semantic_scholar_id,
                "research_tags": row.research_tags or [],
            },
            similarity=float(row.similarity),
            papers=[{
                "id": p.id,
                "title": p.title,
                "year": p.year,
                "venue": p.venue,
                "citation_count": p.citation_count
            } for p in papers]
        ))

    return search_results
