from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi import Security

from app.db.database import Base, engine
from app.db import models
from app.db.database import SessionLocal

from app.schemas.user import UserCreate, UserLogin
from app.schemas.task import TaskCreate, TaskUpdate

from app.core.security import hash_password, verify_password
from app.core.jwt import create_token

from sqlalchemy.orm import Session

from jose import jwt

from fastapi.middleware.cors import CORSMiddleware



security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials=Security(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = jwt.decode(token, "secret", algorithms=["HS256"])

    email = payload.get("sub")

    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для разработки ок
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/tasks")
def create_task(
    task: TaskCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_task = models.Task(
        title=task.title,
        user_id=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    return {"message": "User created"}
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": db_user.email})
    return {"access_token": token}

@app.get("/tasks")
def get_tasks(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(models.Task).filter(models.Task.user_id == user.id).all()

@app.get("/tasks/stats")
def get_stats(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    tasks = db.query(models.Task).filter(models.Task.user_id == user.id).all()

    stats = {
        "todo": 0,
        "in_progress": 0,
        "done": 0
    }

    for t in tasks:
        if t.status == "todo":
            stats["todo"] += 1
        elif t.status == "in_progress":
            stats["in_progress"] += 1
        elif t.status == "done":
            stats["done"] += 1

    return stats

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")


    if task.title is not None:
        db_task.title = task.title
    if task.status is not None:
        db_task.status = task.status

    db.commit()
    db.refresh(db_task)

    return db_task

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}