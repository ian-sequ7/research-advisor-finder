from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector

from app.database import Base

"""
This is going to be the code to make the basic dbs for faculty n their papers

- doing this by using Object relation mapping to define dbs instead or classic insertations
"""

class Faculty(Base):
    
    # setup for CS Faculty Member for the db
    
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, index =True)

    semantic_scholar_id = Column(String(50), unique=True, index=True)

    name = Column(String(255), nullable=False)
    affiliation = Column(String(500))
    homepage = Column(String(500))

    h_index = Column(Integer)
    citation_count = Column(Integer)
    paper_count = Column(Integer)


    research_sumary = Column(Text)
    research_tags = Column(ARRAY(String), nullable=True)

    embedding = Column(Vector(1536))

    created_at = Column(DateTime, server_default=func.now())

    papers = relationship("Paper", back_populates="faculty")

class Paper(Base):
    # setup for a Research paper from a fac member
    
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)

    faculty_id = Column(Integer, ForeignKey("faculty.id"), index=True)

    title = Column(Text, nullable=False)
    abstract = Column(Text)
    year = Column(Integer)
    venue = Column(String(500))
    citation_count = Column(Integer)

    embedding = Column(Vector(1536), nullable=True)

    faculty = relationship("Faculty", back_populates="papers")

