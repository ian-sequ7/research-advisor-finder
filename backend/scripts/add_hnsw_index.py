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

# Fix for Railway/Heroku: postgres:// -> postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    print("Creating HNSW index on faculty.embedding...")
    print("This may take a minute for large tables...")

    conn.execute(text("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS faculty_embedding_hnsw_idx
        ON faculty USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """))
    print("✓ Faculty embedding index created")

    print("Creating HNSW index on papers.embedding...")
    conn.execute(text("""
        CREATE INDEX CONCURRENTLY IF NOT EXISTS papers_embedding_hnsw_idx
        ON papers USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);
    """))
    print("✓ Papers embedding index created")

    print("Analyzing tables...")
    conn.execute(text("ANALYZE faculty;"))
    conn.execute(text("ANALYZE papers;"))
    print("✓ Tables analyzed")

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
