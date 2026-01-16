import sys
import os

if os.path.exists('/app'):
    sys.path.insert(0, '/app')

from sqlalchemy import text
from app.database import engine, Base
from app import models

def init_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    Base.metadata.create_all(bind=engine)
    print("Database initialized with pgvector extension")
    print("Tables created: faculty, papers")

if __name__ == "__main__":
    init_db()
