from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from app.database import Base

class Faculty(Base):
    
    # setup for CS Faculty Member for the db
    
    __tablename__ = "faculty"

    id = Column(Integer, primaryPkey=True, index =True)

    semantic_scholar_id = Column(String(50), unique=True, index=True)

    name = Column(String(255), nullable=False)
    affiliation = Column(String(500))
    homepage = Column(String(500))

    h_index = Column(Integer)
    citation_count = Column(Integer)
    paper_count = Column(Integer)


    research_sumary = Column(Text)
