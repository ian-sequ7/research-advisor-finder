#!/usr/bin/env python3
"""
One-time script to extract and store research tags for all faculty.
Processes faculty without tags, commits after each to allow resumption.
"""
import os
import sys
import time
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Faculty, Paper
from app.services.tag_extractor import extract_research_tags


def populate_all_tags():
    """
    One-time script to extract and store tags for all faculty.
    Processes faculty without tags, commits after each to allow resumption.
    """
    db: Session = SessionLocal()

    try:
        # Get faculty without research_tags
        faculty_without_tags = db.query(Faculty).filter(
            Faculty.research_tags == None
        ).all()

        total = len(faculty_without_tags)
        print(f"Found {total} faculty without research tags")

        if total == 0:
            print("All faculty already have tags. Nothing to do.")
            return

        for i, faculty in enumerate(faculty_without_tags, 1):
            print(f"[{i}/{total}] Processing: {faculty.name}")

            # Get papers for this faculty
            papers = db.query(Paper).filter(
                Paper.faculty_id == faculty.id
            ).order_by(Paper.citation_count.desc()).limit(10).all()

            if not papers:
                print(f"  -> No papers found, skipping")
                # Set empty array instead of NULL to mark as processed
                faculty.research_tags = []
                db.commit()
                continue

            # Convert papers to dicts for tag extractor
            paper_dicts = [
                {"title": p.title, "abstract": p.abstract}
                for p in papers
            ]

            # Extract tags using Claude
            tags = extract_research_tags(paper_dicts)

            if tags:
                print(f"  -> Tags: {tags}")
                faculty.research_tags = tags
            else:
                print(f"  -> No tags extracted")
                faculty.research_tags = []

            # Commit after each faculty to allow resumption
            db.commit()

            # Rate limit: 1 request per second to avoid API limits
            time.sleep(1)

        print(f"\nDone! Processed {total} faculty members.")

    except KeyboardInterrupt:
        print("\n\nInterrupted! Progress has been saved. Run again to resume.")
    except Exception as e:
        print(f"\nError: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    populate_all_tags()
