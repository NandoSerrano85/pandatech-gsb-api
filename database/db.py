import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sys.path.append('../app')
from app.core.config import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Session = sessionmaker(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
