#!/usr/bin/env python3
"""
Migration script to add full-text search support on faculty table.
Adds a tsvector column and GIN index for fast text search.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import engine


def add_fulltext_search():
    """
    Add full-text search support to faculty table:
    1. Add search_vector column (tsvector)
    2. Populate it with existing data
    3. Create GIN index on the column
    4. Create trigger to keep it updated
    """
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'faculty'
            AND column_name = 'search_vector'
        """))

        if result.fetchone():
            print("✓ Column 'search_vector' already exists")
        else:
            print("Adding search_vector column...")
            conn.execute(text("""
                ALTER TABLE faculty
                ADD COLUMN search_vector tsvector
            """))
            print("✓ Added search_vector column")

        print("Populating search_vector with existing data...")
        conn.execute(text("""
            UPDATE faculty
            SET search_vector = to_tsvector('english',
                COALESCE(name, '') || ' ' ||
                COALESCE(research_sumary, '') || ' ' ||
                COALESCE(array_to_string(research_tags, ' '), '')
            )
            WHERE search_vector IS NULL
        """))
        print("✓ Populated search_vector")

        result = conn.execute(text("""
            SELECT indexname
            FROM pg_indexes
            WHERE tablename = 'faculty'
            AND indexname = 'faculty_search_vector_idx'
        """))

        if result.fetchone():
            print("✓ Index 'faculty_search_vector_idx' already exists")
        else:
            print("Creating GIN index...")
            conn.execute(text("""
                CREATE INDEX faculty_search_vector_idx
                ON faculty USING GIN(search_vector)
            """))
            print("✓ Created GIN index")

        print("Creating trigger function...")
        conn.execute(text("""
            CREATE OR REPLACE FUNCTION faculty_search_vector_update()
            RETURNS trigger AS $$
            BEGIN
                NEW.search_vector := to_tsvector('english',
                    COALESCE(NEW.name, '') || ' ' ||
                    COALESCE(NEW.research_sumary, '') || ' ' ||
                    COALESCE(array_to_string(NEW.research_tags, ' '), '')
                );
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql
        """))
        print("✓ Created trigger function")

        result = conn.execute(text("""
            SELECT tgname
            FROM pg_trigger
            WHERE tgname = 'faculty_search_vector_trigger'
        """))

        if result.fetchone():
            print("✓ Trigger already exists")
        else:
            print("Creating trigger...")
            conn.execute(text("""
                CREATE TRIGGER faculty_search_vector_trigger
                BEFORE INSERT OR UPDATE ON faculty
                FOR EACH ROW
                EXECUTE FUNCTION faculty_search_vector_update()
            """))
            print("✓ Created trigger")

        conn.commit()


if __name__ == "__main__":
    try:
        add_fulltext_search()
        print("\n✓ Migration completed successfully!")
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        sys.exit(1)
