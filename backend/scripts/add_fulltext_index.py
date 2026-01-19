#!/usr/bin/env python3
"""
Migration script to add GIN index for full-text search on faculty table.
This improves performance of PostgreSQL full-text search queries.
"""

import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import engine


def add_fulltext_index():
    """
    Create GIN index for full-text search on faculty table.
    Combines name, research_summary, and research_tags fields.
    """
    with engine.connect() as conn:
        # Check if index already exists
        result = conn.execute(text("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'faculty'
            AND indexname = 'faculty_fulltext_idx'
        """))

        if result.fetchone():
            print("✓ Index 'faculty_fulltext_idx' already exists, skipping creation")
            return

        print("Creating GIN index for full-text search...")

        conn.execute(text("""
            CREATE INDEX faculty_fulltext_idx ON faculty
            USING GIN(
                to_tsvector('english',
                    name || ' ' ||
                    COALESCE(research_sumary, '') || ' ' ||
                    COALESCE(array_to_string(research_tags, ' '), '')
                )
            )
        """))

        conn.commit()
        print("✓ Successfully created 'faculty_fulltext_idx' index")


if __name__ == "__main__":
    try:
        add_fulltext_index()
        print("\nMigration completed successfully!")
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        sys.exit(1)
