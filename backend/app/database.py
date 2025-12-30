import os
from sqlalchemy import create_engine
from sqlalchemy import sessionmaker, declarative_base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/advisor_finder"
)
#db creation
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=FALSE, bind=engine)

Base = declarative_base()

 #use dep injection for db to prevent errors
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
