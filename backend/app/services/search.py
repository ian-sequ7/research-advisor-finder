from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models import Paper
from app.schemas import SearchResult

# Search configuration constants
RRF_K_CONSTANT = 60  # Standard constant for Reciprocal Rank Fusion
FULLTEXT_SEARCH_LIMIT = 50  # Default limit for full-text search results
VECTOR_SEARCH_LIMIT = 50  # Default limit for vector similarity search results
MAX_PAPERS_PER_FACULTY = 5  # Maximum number of top papers to include per faculty member


def search_faculty_fulltext(
    db: Session,
    query: str,
    limit: int = 50,
    min_h_index: int = 0,
    universities: list[str] | None = None,
) -> list[tuple[int, float]]:
    """
    Search faculty using PostgreSQL full-text search.
    Returns list of (faculty_id, ts_rank_score) tuples.
    """
    where_clauses = ["h_index >= :min_h"]
    params = {
        "query": query,
        "min_h": min_h_index,
        "limit": limit
    }

    if universities:
        where_clauses.append("affiliation = ANY(:universities)")
        params["universities"] = universities

    where_sql = " AND ".join(where_clauses)

    results = db.execute(
        text(f"""
            SELECT id, ts_rank(search_vector, plainto_tsquery('english', :query)) as rank
            FROM faculty
            WHERE search_vector @@ plainto_tsquery('english', :query)
              AND {where_sql}
            ORDER BY rank DESC
            LIMIT :limit
        """),
        params
    ).fetchall()

    return [(row.id, float(row.rank)) for row in results]


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

    # Group papers by faculty_id, keeping top papers per faculty
    papers_by_faculty = {}
    for paper in papers_query:
        if paper.faculty_id not in papers_by_faculty:
            papers_by_faculty[paper.faculty_id] = []
        if len(papers_by_faculty[paper.faculty_id]) < MAX_PAPERS_PER_FACULTY:
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


def search_faculty_hybrid(
    db: Session,
    query: str,
    embedding: list[float],
    limit: int = 10,
    min_h_index: int = 0,
    universities: list[str] | None = None,
    k: int = RRF_K_CONSTANT
) -> list[SearchResult]:
    """
    Hybrid search combining BM25 full-text search with vector semantic search using RRF.

    RRF (Reciprocal Rank Fusion) formula: score = sum(1 / (k + rank))
    where k=60 is the standard constant for search result fusion.
    """
    # Get vector search results (semantic similarity)
    where_clauses = ["embedding IS NOT NULL", "h_index >= :min_h"]
    params = {
        "embedding": str(embedding),
        "min_h": min_h_index,
        "vector_limit": VECTOR_SEARCH_LIMIT
    }

    if universities:
        where_clauses.append("affiliation = ANY(:universities)")
        params["universities"] = universities

    where_sql = " AND ".join(where_clauses)

    vector_results = db.execute(
        text(f"""
            SELECT
                id, name, affiliation, h_index, paper_count,
                semantic_scholar_id, research_tags,
                1 - (embedding <=> :embedding) as similarity
            FROM faculty
            WHERE {where_sql}
            ORDER BY embedding <=> :embedding
            LIMIT :vector_limit
        """),
        params
    ).fetchall()

    # Get full-text search results
    fulltext_results = search_faculty_fulltext(
        db=db,
        query=query,
        limit=FULLTEXT_SEARCH_LIMIT,
        min_h_index=min_h_index,
        universities=universities
    )

    # Build rank dictionaries
    vector_ranks = {row.id: rank + 1 for rank, row in enumerate(vector_results)}
    fulltext_ranks = {faculty_id: rank + 1 for rank, (faculty_id, _) in enumerate(fulltext_results)}

    # WHY: Combine all unique faculty IDs from both searches for RRF scoring
    all_faculty_ids = set(vector_ranks.keys()) | set(fulltext_ranks.keys())

    # Calculate RRF scores
    rrf_scores = {}
    for faculty_id in all_faculty_ids:
        score = 0.0
        if faculty_id in vector_ranks:
            score += 1.0 / (k + vector_ranks[faculty_id])
        if faculty_id in fulltext_ranks:
            score += 1.0 / (k + fulltext_ranks[faculty_id])
        rrf_scores[faculty_id] = score

    # Sort by RRF score and get top results
    top_faculty_ids = sorted(rrf_scores.keys(), key=lambda x: rrf_scores[x], reverse=True)[:limit]

    if not top_faculty_ids:
        return []

    # Fetch full faculty details for top results
    faculty_details = db.execute(
        text("""
            SELECT
                id, name, affiliation, h_index, paper_count,
                semantic_scholar_id, research_tags
            FROM faculty
            WHERE id = ANY(:faculty_ids)
        """),
        {"faculty_ids": top_faculty_ids}
    ).fetchall()

    # Create lookup for faculty details
    faculty_map = {row.id: row for row in faculty_details}

    # Batch fetch papers for all faculty
    papers_query = (
        db.query(Paper)
        .filter(Paper.faculty_id.in_(top_faculty_ids))
        .order_by(Paper.citation_count.desc())
        .all()
    )

    # Group papers by faculty_id, keeping top papers per faculty
    papers_by_faculty = {}
    for paper in papers_query:
        if paper.faculty_id not in papers_by_faculty:
            papers_by_faculty[paper.faculty_id] = []
        if len(papers_by_faculty[paper.faculty_id]) < MAX_PAPERS_PER_FACULTY:
            papers_by_faculty[paper.faculty_id].append(paper)

    # Build response maintaining RRF rank order
    search_results = []
    for faculty_id in top_faculty_ids:
        if faculty_id not in faculty_map:
            continue

        row = faculty_map[faculty_id]
        papers = papers_by_faculty.get(faculty_id, [])

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
            similarity=float(rrf_scores[faculty_id]),
            papers=[{
                "id": p.id,
                "title": p.title,
                "year": p.year,
                "venue": p.venue,
                "citation_count": p.citation_count
            } for p in papers]
        ))

    return search_results
