from sqlalchemy import Column, Integer, String, LargeBinary
from database.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(LargeBinary)
    store_url = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    api_access_token = Column(String, unique=True, index=True)
    api_version = Column(String, unique=True, index=True)