"""
Add HNSW index to faculty and papers embedding columns for faster vector search.
Run this once on your production database.

Usage:
    python scripts/add_hnsw_index.py
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    print("Creating HNSW index on faculty.embedding...")
    print("This may take a minute for large tables...")

    # Create HNSW index on faculty embeddings
    conn.execute(text("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS faculty_embedding_hnsw_idx
        ON faculty USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """))
    conn.commit()
    print("✓ Faculty embedding index created")

    print("Creating HNSW index on papers.embedding...")
    conn.execute(text("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS papers_embedding_hnsw_idx
        ON papers USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """))
    conn.commit()
    print("✓ Papers embedding index created")

    # Analyze tables to update query planner statistics
    print("Analyzing tables...")
    conn.execute(text("ANALYZE faculty;"))
    conn.execute(text("ANALYZE papers;"))
    conn.commit()
    print("✓ Tables analyzed")

    # Check index sizes
    result = conn.execute(text("""
        SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass)) as size
        FROM pg_indexes
        WHERE tablename IN ('faculty', 'papers')
        AND indexname LIKE '%embedding%';
    """))

    print("\nIndex sizes:")
    for row in result:
        print(f"  {row[0]}: {row[1]}")

    print("\n✅ Done! Vector searches will now use HNSW indexes.")
