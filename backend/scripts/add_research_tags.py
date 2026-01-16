import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not set")
    exit(1)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)

def add_research_tags_column():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'faculty' AND column_name = 'research_tags'
        """))

        if result.fetchone() is None:
            print("Adding research_tags column to faculty table...")
            conn.execute(text("ALTER TABLE faculty ADD COLUMN research_tags TEXT[]"))
            conn.commit()
            print("Column added successfully!")
        else:
            print("research_tags column already exists.")

if __name__ == "__main__":
    add_research_tags_column()
