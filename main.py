from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import TEXT, VARCHAR, LargeBinary, Column, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = FastAPI()

DATABASE_URL = 'postgresql://postgres:test123@localhost:5432/harmoniz-streaming-music'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
db = SessionLocal()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(TEXT, primary_key = True)
    name = Column(VARCHAR(100))
    email = Column(VARCHAR(100))
    password = Column(LargeBinary)

@app.post('/signup')
def signup_user(user: UserCreate):
    # EXTRACT DATA THATS COMING FROM REQ
    print(user.name)
    print(user.email)
    print(user.password)
    
    # CHECK IF USER ALREADY EXIST IN DB
    # ADD THE USER TO THE DB
    pass