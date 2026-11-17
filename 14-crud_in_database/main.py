from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import Column, Integer, String
from fastapi import FastAPI, Depends
from fastapi import *
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

# create API
@app.post("/todos")
def create_todo(title: str, db: Session = Depends(get_db)):
    todo = Todo(title=title, completed="False")
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "message" : "Todo created",
        "data" : todo
    }

# read All data
@app.get("/todos")
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()

    return{
        "total" : len(todos),
        "data" : todos
    }

# read by ID
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with id {todo_id} not found")
    return{
        "message" : f"todo with id {todo_id} is retrieved",
        "data" : todo
    }

# update API
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, title: str, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with id {todo_id} not found")

    todo.title = title
    db.commit()
    db.refresh(todo)

    return{
        "message" : "Db got updated",
        "data" : todo
    }

# delete API
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id==todo_id).first()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo with id {todo_id} not found")
        
    db.delete(todo)
    db.commit()

    return{
        "message" : "todo deleted"
    }
