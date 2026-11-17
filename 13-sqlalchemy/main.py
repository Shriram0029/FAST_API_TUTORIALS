from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column, Integer, String
from fastapi import FastAPI, Depends

app = FastAPI()

# Database URL
DATABASE_URL = "sqlite:///./test.db"

# Engine create ( DB CONNECTION )
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session ( for DB Operations )
sessionLocal = sessionmaker(bind=engine)

# Base model
Base = declarative_base()

# Table Model
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(String, index=True)

# Table create
Base.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/home")
def home(db: Session = Depends(get_db)):
    return{
        "message" : "DB Connection Successful"
    }
