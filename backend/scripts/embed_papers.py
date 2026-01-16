import sys
import os
import time

# Support both Docker (/app) and local execution
sys.path.insert(0, '/app')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from openai import OpenAI
from app.database import SessionLocal, engine
from app.models import Paper

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def ensure_embedding_column():
    """Add embedding column to papers table if it doesn't exist."""
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'papers' AND column_name = 'embedding'
        """))
        if result.fetchone() is None:
            print("Adding embedding column to papers table...")
            conn.execute(text("ALTER TABLE papers ADD COLUMN embedding vector(1536)"))
            conn.commit()
            print("Column added!")
        else:
            print("Embedding column already exists.")

def get_embedding(text: str) -> list[float]:
    """Get embedding using OpenAI text-embedding-3-small."""
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def build_paper_text(paper: Paper) -> str:
    """Build text for embedding from paper title and abstract."""
    parts = [paper.title]

    if paper.abstract:
        # Truncate very long abstracts to stay within token limits
        abstract = paper.abstract[:2000]
        parts.append(abstract)

    if paper.venue:
        parts.append(f"Published in: {paper.venue}")

    return "\n".join(parts)

def embed_all_papers(batch_size: int = 50):
    """Generate embeddings for all papers without embeddings that have abstracts."""
    db = SessionLocal()

    try:
        # Get papers without embeddings that have abstracts
        papers = db.query(Paper).filter(
            Paper.embedding.is_(None),
            Paper.abstract.isnot(None),
            Paper.abstract != ""
        ).all()

        total = len(papers)
        print(f"Found {total} papers to embed")

        if total == 0:
            print("No papers need embedding!")
            return

        embedded = 0
        errors = 0
        start_time = time.time()

        for i, paper in enumerate(papers):
            try:
                # Build text and get embedding
                text = build_paper_text(paper)
                embedding = get_embedding(text)

                # Save embedding
                paper.embedding = embedding
                embedded += 1

                # Commit in batches
                if (i + 1) % batch_size == 0:
                    db.commit()
                    elapsed = time.time() - start_time
                    rate = embedded / elapsed
                    remaining = (total - i - 1) / rate if rate > 0 else 0
                    print(f"Progress: {i + 1}/{total} ({embedded} embedded, {errors} errors) - ETA: {remaining:.1f}s")

            except Exception as e:
                print(f"  Error embedding paper {paper.id}: {e}")
                errors += 1
                continue

        # Final commit
        db.commit()

        elapsed = time.time() - start_time
        print(f"\nDone! Embedded {embedded} papers in {elapsed:.1f}s ({errors} errors)")

    finally:
        db.close()


def count_papers():
    """Count papers that need embedding."""
    db = SessionLocal()
    try:
        need_embedding = db.query(Paper).filter(
            Paper.embedding.is_(None),
            Paper.abstract.isnot(None),
            Paper.abstract != ""
        ).count()

        already_embedded = db.query(Paper).filter(
            Paper.embedding.isnot(None)
        ).count()

        no_abstract = db.query(Paper).filter(
            (Paper.abstract.is_(None)) | (Paper.abstract == "")
        ).count()

        print(f"Papers needing embedding: {need_embedding}")
        print(f"Papers already embedded: {already_embedded}")
        print(f"Papers without abstract: {no_abstract}")

    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Embed paper abstracts")
    parser.add_argument("--count", action="store_true", help="Just count papers")
    parser.add_argument("--batch-size", type=int, default=50, help="Commit batch size")
    args = parser.parse_args()

    # Ensure the embedding column exists before doing anything
    ensure_embedding_column()

    if args.count:
        count_papers()
    else:
        embed_all_papers(batch_size=args.batch_size)
