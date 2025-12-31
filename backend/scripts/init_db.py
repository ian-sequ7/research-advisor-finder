import sys
sys.path.insert(0, '/app')

from sqlalchemy import text
from app.database import engine, Base
from app import models

def init_db():
